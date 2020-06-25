# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : ldap3_interface.py
# Author            : Balazs Lendvay
# Date created      : 2020.06.21
# Purpose           : LDAP query file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2020.06.21  Lendvay     1      Initial file
# **********************************************************************;

try:
    import ldap3
    from ldap3 import AUTO_BIND_NO_TLS, AUTO_BIND_TLS_BEFORE_BIND
    import ldap3.core.exceptions
    import argparse
except ImportError:
    # logger.info('LDAP3 package not installed, LDAP authentication disabled.')
    print('[x] LDAP3 package or argparse not installed, LDAP authentication disabled.')
    # exit()


class LDAP_interface():

    def __init__(self, pUSERNAME, pPASSWORD, pDOMAIN, pSERVER):
        self.ldapuser = pUSERNAME
        self.ldappass = pPASSWORD
        self.ldapdomain = pDOMAIN
        self.ldapserver = pSERVER

    def ldap_connect(self):
        pusername = self.ldapuser
        ppassword = self.ldappass
        pldapuri = self.ldapserver
        pdomain = self.ldapdomain

        uri = pldapuri
        if uri.startswith('ldaps://'):
            host = uri[8:]
            ssl = True
            port = 636
        elif uri.startswith('ldap://'):
            host = uri[7:]
            ssl = False
            port = 389
        else:
            raise ValueError('Invalid LDAP URI: {}'.format(uri))
        server = ldap3.Server(host, port=port, use_ssl=ssl, get_info=ldap3.ALL)
        try:
            theuser = '{}\{}'.format(pdomain, pusername)
            conn = None
            if ssl:
                conn = ldap3.Connection(server, user=theuser,
                                      password=ppassword, auto_bind=ldap3.AUTO_BIND_TLS_BEFORE_BIND)
            else:
                conn = ldap3.Connection(server, user=theuser,
                                        password=ppassword, auto_bind=ldap3.AUTO_BIND_NO_TLS)
            return conn
        except ldap3.core.exceptions.LDAPExceptionError as exc:
            print('[x] Failed to authenticate user ' + pusername + ' using LDAP: {}.'.format(str(exc)))
            exit()
            return False

    def ldap_disconnect(self, pconn):
        pconn.unbind()

    def ldap_query(self, pconn, pquery):
        retval = list()
        try:
            searchok = pconn.extend.standard.paged_search(**pquery)
            for searchitems in searchok:
                retdict = dict()
                for attrname, attrvalue in searchitems['attributes'].items():
                    retdict[attrname] = attrvalue
                retval.append(retdict)
        except Exception as e:
            print("[x] Error searching %s" % e)
        # https: // ldap3.readthedocs.io / en / latest / tutorial_abstraction_reader.html
        return retval

    def ldap_query_csv(self, pquery, pdelimiter=',', noheader=False):
        myconn = self.ldap_connect()
        query_res = self.ldap_query(pconn=myconn, pquery=pquery)
        # print(query_res)
        runonce = True
        retval = str()
        for item in query_res:
            onelineheader = str()
            if runonce and not noheader:
                for keyval in item.keys():
                    onelineheader = "%s%s%s" % (onelineheader, pdelimiter, keyval)
                runonce = False
                # print(onelineheader[1:])
                retval = "%s\n" % onelineheader[1:]
            oneline = str()
            for akey,aval in item.items():
                oneline = "%s%s%s" % (oneline, pdelimiter, aval)
            retval = "%s%s\n" % (retval, oneline[1:])
            # print(onelineheader)
            # print(onelinedata)
        self.ldap_disconnect(myconn)
        return retval


    def ldap_query_value(self, pquery, noheader=False):
        myconn = self.ldap_connect()
        query_res = self.ldap_query(pconn=myconn, pquery=pquery)
        retval = str()
        try:
            for item in query_res:
                for akey, avalue in item.items():
                    retval = avalue
        except Exception as e:
            if not noheader:
                print("[x] No results")
        self.ldap_disconnect(myconn)
        return retval

    def ldap_query_custom(self, pquery):
        myconn = self.ldap_connect()
        retvallist = self.ldap_query(pconn=myconn, pquery=pquery)
        retval = None
        if len(retvallist) >= 1:
            retval = retvallist[0]
        self.ldap_disconnect(myconn)
        return retval

    def test(self, str1):
        return str1

def build_parser():
    parser = argparse.ArgumentParser(description='Query an LDAP server for information.',
                                     usage='ldap_query [options]')
    parser.add_argument('-u', '--username', action='store', type=str, help='LDAP username',
                        dest="param_username")
    parser.add_argument('-q', '--queryvalue', action='store_true', help='Print last value',
                        dest="param_queryvalue")
    parser.add_argument('-c', '--querycsv', action='store_true', help='Print all value in csv format',
                        dest="param_querycsv")
    parser.add_argument('-n', '--noheader', action='store_true', help='Do not print header',
                        dest="param_noheader")
    parser.add_argument('-p', '--password', action='store', type=str, help='LDAP password',
                        dest="param_password")
    parser.add_argument('-s', '--server', action='store', type=str, help='LDAP server',
                        dest="param_server")
    parser.add_argument('-d', '--domain', action='store', type=str, help='LDAP domain',
                        dest="param_domain")
    parser.add_argument('--searchbasedn', action='store', type=str, help='LDAP search base DN',
                        dest="param_searchbasedn")
    parser.add_argument('--searchfilter', action='store', type=str, help='LDAP search filter',
                        dest="param_searchfilter")
    parser.add_argument('--searchattributes', action='store', type=str, help='LDAP search attributes',
                        dest="param_searchattributes")
    parser.add_argument('--searchpagesize', action='store', type=str, help='LDAP search page size',
                        dest="param_searchpagesize")

    # parser.add_argument('--dcs', action='store_true', help='List domain controllers', dest="param_dcs")
    # parser.add_argument('-r', '--rescan', action='store_true', help='Re-Scan the resource')

    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    args = build_parser()
    # any param
    # pnum=0
    # for i in args.keys():
    #     if args[i]:
    #         pnum += 1
    # if pnum == 0:
    #     print("Use '-h' to get command line help")

    myusername = "administrator"
    mypassword = "Password1."
    myserver = "ldap://192.168.11.72"
    mydomain = 'lendvay'
    mysearchbasedn = 'ou=Test,dc=lendvay,dc=local'
    mysearchfilter = '(objectclass=Person)'
    # mysearchfilter = '(& (objectCategory=person)(objectClass=user)(sAMAccountName=test1))'
    mysearchattributes = ['sAMAccountName', 'pwdLastSet']
    mysearchpagesize = 5

    aquery = {'search_base': mysearchbasedn,
                    'search_filter': mysearchfilter,
                    'attributes': mysearchattributes,
                    'paged_size': mysearchpagesize,
                    'generator': False,
                    }

    aconnection =LDAP_interface(pUSERNAME=myusername,
                                pPASSWORD=mypassword,
                                pSERVER=myserver,
                                pDOMAIN=mydomain,
                                )
    # aconn = aconnection.ldap_connect()
    # ares = aconnection.ldap_query(aconn, aquery)
    # aconnection.ldap_disconnect(aconn)
    # print(ares)
    output = None
    if args['param_username']:
        myusername = args['param_username']
    if args['param_password']:
        mypassword = args['param_password']
    if args['param_server']:
        myserver = args['param_server']
    if args['param_domain']:
        mydomain = args['param_domain']
    if args['param_searchbasedn']:
        mysearchbasedn = args['param_searchbasedn']
    if args['param_searchfilter']:
        mysearchfilter = args['param_searchfilter']
    if args['param_searchattributes']:
        mysearchattributes = args['param_searchattributes']
    if args['param_searchpagesize']:
        mysearchpagesize = args['param_searchpagesize']

    if args['param_queryvalue']:
        if args['param_noheader']:
            output = aconnection.ldap_query_value(pquery=aquery, noheader=True)
        else:
            output = aconnection.ldap_query_value(pquery=aquery, noheader=False)

    if args['param_querycsv']:
        if args['param_noheader']:
            output = aconnection.ldap_query_csv(pquery=aquery, noheader=True)
        else:
            output = aconnection.ldap_query_csv(pquery=aquery, noheader=False)

    print(output)
