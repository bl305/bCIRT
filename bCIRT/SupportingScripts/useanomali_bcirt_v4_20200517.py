#!/usr/bin/python3
# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : scripts/useanomali_bcirt_v4.py
# Author            : Balazs Lendvay
# Date created      : 2019.08.18
# Purpose           : Anomali query script for the bCIRT
# Revision History  : v2
# Date        Author      Ref    Description
# 2019.08.18  Lendvay     1      Initial file
# 2020.05.17  Lendvay     2      Added submit IoC functions
# **********************************************************************;

import requests
import logging as log
from sys import exit
from collections.abc import Iterable
import argparse
import json

apiuser = '$apiuser$'
apikey = '$apikey$'

query_api1_url = 'https://api.threatstream.com/api/v1'
query_api2_url = 'https://api.threatstream.com/api/v2'
# log.basicConfig(format='%(message)s', level=log.INFO)
# /api/v1/impact


class UseAnomali():
    def __init__(self, showurl=False):
        # self.issuccess = False
        self.showurl = showurl
        self.itypes = [
            'actor_ip', 'actor_ipv6', 'adware_domain', 'adware_registry_key', 'anon_proxy', 'anon_proxy_ipv6',
            'anon_vpn',
            'anon_vpn_ipv6', 'apt_domain', 'apt_email', 'apt_file_name', 'apt_file_path', 'apt_ip', 'apt_ipv6',
            'apt_md5',
            'apt_mta', 'apt_mutex', 'apt_registry_key', 'apt_service_description', 'apt_service_displayname',
            'apt_service_name',
            'apt_ssdeep', 'apt_subject', 'apt_ua', 'apt_url', 'bot_ip', 'bot_ipv6', 'brute_ip', 'brute_ipv6',
            'c2_domain', 'c2_ip',
            'c2_ipv6', 'c2_url', 'comm_proxy_domain', 'comm_proxy_ip', 'compromised_domain', 'compromised_email',
            'compromised_ip',
            'compromised_ipv6', 'compromised_url', 'crypto_hash', 'crypto_ip', 'crypto_pool', 'crypto_url',
            'crypto_wallet', 'ddos_ip',
            'ddos_ipv6', 'disposable_email_domain', 'dyn_dns', 'exfil_domain', 'exfil_ip', 'exfil_ipv6', 'exfil_url',
            'exploit_domain',
            'exploit_ip', 'exploit_ipv6', 'exploit_url', 'free_email_domain', 'geolocation_url', 'hack_tool', 'i2p_ip',
            'i2p_ipv6',
            'ipcheck_url', 'mal_domain', 'mal_email', 'mal_file_name', 'mal_file_path', 'mal_ip', 'mal_ipv6', 'mal_md5',
            'mal_mutex',
            'mal_registry_key', 'mal_service_description', 'mal_service_displayname', 'mal_service_name', 'mal_ssdeep',
            'mal_sslcert_sh1', 'mal_ua', 'mal_url', 'p2pcnc', 'p2pcnc_ipv6', 'parked_domain', 'parked_ip',
            'parked_ipv6', 'parked_url',
            'pastesite_url', 'phish_domain', 'phish_email', 'phish_ip', 'phish_ipv6', 'phish_md5', 'phish_url',
            'proxy_ip', 'proxy_ipv6',
            'scan_ip', 'scan_ipv6', 'sinkhole_domain', 'sinkhole_ip', 'sinkhole_ipv6', 'sinkhole_ipv6', 'spam_domain',
            'spam_email',
            'spam_ip', 'spam_ipv6', 'spam_mta', 'spam_url', 'speedtest_url', 'ssh_ip', 'ssh_ipv6',
            'ssl_cert_serial_number',
            'suppress', 'suspicious_domain', 'suspicious_email', 'suspicious_ip', 'suspicious_reg_email',
            'suspicious_url',
            'tor_ip', 'tor_ipv6', 'torrent_tracker_url', 'vpn_domain', 'vps_ip', 'vps_ipv6', 'whois_bulk_reg_email',
            'whois_privacy_domain', 'whois_privacy_email'
        ]

        self.examples = [
            'python3 useanomali.py -r intelligence -s 195.22.26.248',
            'python3 useanomaly.py -r intelligence --intelstatus active -s covid19',
            'python3 useanomaly.py -r intelligence 4DA1F312A214C07143ABEEAFB695D904',
            'python3 useanomaly.py -r intelligence www.ifferfsodp9ifjaposdfjhgosurijfaewrwergwea.com',
            'python3 useanomaly.py -sendiocvalue "176.10.99.200" - -sendioctype phish --sendioctag bcirt:red,phish:red',
        ]

    def gettypes(self):
        for item in self.itypes:
            print(item)

    def showexamples(self):
        for item in self.examples:
            print(item)

    # https://api.threatstream.com/api/v1/threat_model_search/&limit=100
    def query_api_intel(self, papiurl, papiuser, papikey, presource, pflags=''):
        # http_outcode = None
        metadata_id = 'meta'
        result_id = 'objects'
        url = '{}/{}/?username={}&api_key={}{}'.format(papiurl, presource, papiuser, papikey, pflags)
        if self.showurl:
            print(url)
            exit(0)
        try:
            http_req = requests.get(url, headers={'ACCEPT': 'application/json, text/html'})
            if http_req.status_code == 200:
                resmeta = http_req.json()[metadata_id]
                res = http_req.json()[result_id]
                # print("QM:%s"%(resmeta))
                # print("QR:%s" % (res))
                return (resmeta, res)  # Return JSON Blob
                # return (http_req.json()['objects'])  # Return JSON Blob
            elif http_req.status_code == 401:
                log.error('Access Denied. Check API Credentials')
                exit(0)
            else:
                log.info('API Connection Failure. Status code: {}'.format(http_req.status_code))
        except Exception as err:
            log.error('API Access Error: {}'.format(err))
            exit(0)

    def post_api(self, papiurl, papiuser, papikey, presource, pflags=''):
        # print("url: %s\nuser: %s\nkey: %s\nres: %s\npflags: %s\n" % (papiurl, papiuser, papikey, presource, pflags))
        # http_outcode = None
        metadata_id = 'meta'
        result_id = 'objects'
        url = '{}/{}/?username={}&api_key={}'.format(papiurl, presource, papiuser, papikey)
        if self.showurl:
            print("POST data: %s" % pflags)
            print(url)
            exit(0)
        http_req = requests.post(url, pflags)
        try:
            if http_req.status_code == 200:
                resmeta = http_req.json()['job_id']
                res = http_req.json()['success']
                # print("QM:%s"%(resmeta))
                # print("QR:%s" % (res))
                # print(resmeta)
                # print(res)
                return (resmeta, res)# Return JSON Blob
                # return (http_req.json()['objects'])  # Return JSON Blob
            elif http_req.status_code == 202:
                # print("Submission accepted")
                # resmeta = http_req.json()[job_id]
                resmeta = http_req.json()['import_session_id']
                res = http_req.json()['success']
                return (resmeta, res)# Return JSON Blob
            elif http_req.status_code == 401:
                log.error('Access Denied. Check API Credentials')
                exit(0)
            else:
                log.info('API Connection Failure. Status code: {}'.format(http_req.status_code))
        except Exception as err:
            log.error('API Access Error: {}'.format(err))
            exit(0)

    def get_intel(self, papiurl, papiuser, papikey, pinteltype=None, psearchvalue=None,
                  psearchregex=False, psearchregexp=False, psearchcontains=False,
                  psearchexact=False, psearchstartswith=False,
                  plimit=3, pstatus=None,
                  pextend_source=True):
        r = []
        m = []
        log.info('Downloading intelligence: \n')
        # INTEL = {'c2_domain', 'bot_ip'}  # filter to itype
        pflags = ''
        if not psearchregex \
                and not psearchregexp \
                and not psearchcontains \
                and not psearchexact \
                and not psearchstartswith:
            psearchcontains = True
        if psearchregex and psearchvalue:
            pflags = '{}&value__regex={}'.format(pflags, psearchvalue)
        elif psearchregexp and psearchvalue:
            pflags = '{}&value__regexp={}'.format(pflags, psearchvalue)
        elif psearchcontains and psearchvalue:
            pflags = '{}&value__contains={}'.format(pflags, psearchvalue)
        elif psearchstartswith and psearchvalue:
            pflags = '{}&value__startswith={}'.format(pflags, psearchvalue)
        elif psearchexact and psearchvalue:
            pflags = '{}&value={}'.format(pflags, psearchvalue)
        if plimit:
            pflags = '{}&limit={}'.format(pflags, plimit)
        if pstatus:
            pflags = '{}&status={}'.format(pflags, pstatus)
        if pextend_source:
            pflags = '{}&extend_source=true'.format(pflags)
        else:
            pflags = '{}&extend_source=false'.format(pflags)
        if isinstance(pinteltype, Iterable):
            for itype in pinteltype:
                pflagstmp = '{}&itype={}'.format(pflags, itype)
                (resmeta, res) = self.query_api_intel(papiurl=papiurl, papiuser=papiuser, papikey=papikey,
                                                      presource='intelligence', pflags=pflagstmp)
                if len(resmeta) > 0:
                    m.append(resmeta)
                if len(res) > 0:
                    r.append(res)
        else:
            (resmeta, res) = self.query_api_intel(papiurl=papiurl, papiuser=papiuser, papikey=papikey,
                                                  presource='intelligence', pflags=pflags)
            # drop the next field as it contains the API key
            resmetaclean = dict()
            resmetaclean['limit'] = resmeta['limit']
            resmetaclean['total_count'] = resmeta['total_count']
            if len(resmeta) > 0:
                m.append(resmetaclean)
            if len(res) > 0:
                r.append(res)
            # r = {'Result': 'No Data'}
        print("searchtext: '%s'" % psearchvalue)
        # print("M:%s"%(m))
        # print("R:%s"%(r))
        return (m, r)

    def format_output(self, jsonblobmeta, jsonblobresult, ptype):
        r = ""
        m = ""
        if ptype == "intel":
            resultcount = 0
            if jsonblobmeta and isinstance(jsonblobmeta, list):
                for line in jsonblobmeta:
                    # print("LINE:%s"%(line))
                    resultcount = line['total_count']
                    for k, v in line.items():
                        # if not v: continue
                        # print(k,v)
                        m += "{}: {}\n".format(k, v)
            else:
                m = {'Result': 'Not parsable MetaData or No data'}
            if resultcount == 0:
                r = {'Result': 'Not results'}
            elif jsonblobresult and isinstance(jsonblobresult, list) and (resultcount != 0 and jsonblobresult != []):
                for line in jsonblobresult[0]:
                    # print("LINE:%s"%(line))
                    for k, v in line.items():
                        if not v:
                            continue
                        r += "{}: {}\n".format(k, v)
            else:
                r = {'Result': 'Not parsable Data or No data'}
            # print("m:%s r:%s\n"%(m,r))
        elif ptype == "iocsubmission":
            m = {'ImportSessionID': jsonblobmeta}
            r = {'Success': jsonblobresult}
        return (m, r)

# ####################################################
# example: curl -X POST
# 'https://api.threatstream.com/api/v1/intelligence/import/?username=<user>&api_1key=<key>' 
# -F "threat_type=malware" -F "datatext=<text_to_parse_and_import>" -F "classification=private" -F "confidence=90"
    # -F 'tags=[{"name":"bcirt","tlp":"red"},{"name":"phishing", "tlp":"red"}]'
# threat_types
# mal_url, mal_ip, mal_domain, mal_email

    def send_ioc(self, papiurl, papiuser, papikey, pthreattype='malware',
                 pdatatext="", pclassification='private', pconfidence=90,
                 ptags='[{"name":"bcirt","tlp":"red"},{"name":"phishing","tlp":"red"}]'):
        # print("url: %s, user: %s,key: %s,pthreattype: %s,pdatatext: %s,pclass: %s,pconf: %s" % (papiurl,papiuser,
        # papikey,pthreattype,pdatatext, pclassification,pconfidence))

        # ptags='[{"name":"bcirt","tlp":"red"}]'
        # ptags='[{"name":"bcirt","tlp":"red"},{"name":"phishing", "tlp":"red"}]'
        # ptags='[{"name":"test","tlp":"red"},{"name":"phishing", "tlp":"red"}]'
        # r = []
        # m = []
        log.info('Sending IoC: \n')
        # INTEL = {'c2_domain', 'bot_ip'}  # filter to itype
        # -F "threat_type=mal_url" -F "datatext=<text_to_parse_and_import>" -F "classification=private"
        # -F "confidence=90" -F 'tags=[{"name":"bcirt","tlp":"red"},{"name":"phishing", "tlp":"red"}]'
        pflags = dict()
        # pflags = '{}&threat_type={}'.format(pflags, pthreattype)
        # pflags = '{}&datatext={}'.format(pflags, pdatatext)
        # pflags = '{}&classificaiton={}'.format(pflags, pclassification)
        # pflags = '{}&confidence={}'.format(pflags, pconfidence)
        # pflags = '{}&tags={}'.format(pflags, ptags)
        # pflags = '&threat_type=malware&datatext=145.14.145.16&classification=private&confidence=10'
        # #&tags=\'[{"name":"bcirt","tlp":"red"},{"name":"phishing_Lear", "tlp":"red"}]\''
        pflags['threat_type'] = pthreattype
        pflags['datatext'] = pdatatext
        pflags['classification'] = pclassification
        pflags['confidence'] = pconfidence
        pflags['tags'] = ptags
        (resmeta, res) = self.post_api(papiurl=papiurl, papiuser=papiuser, papikey=papikey,
                                       presource='intelligence/import', pflags=pflags)
        print("IoC: %s" % pflags)

        # if len(resmeta) > 0:
        #     m.append(resmeta)
        # if len(res) > 0:
        #     r.append(res)
        # r = {'Result': 'No Data'}
        # print("M:%s" % (resmeta))
        # print("R:%s" % (res))
        return (resmeta, res)


def build_parser():
    parser = argparse.ArgumentParser(description='Use Anomali', usage='useanomali [options]')
    # parser.add_argument("input", help="Search term to look for")
    parser.add_argument('-t', '--listinteltypes', action='store_true', help='List intelligence types',
                        dest="input-listinteltype")
    parser.add_argument('-j', '--json', action='store_true', help='Output in JSON', dest="json")
    parser.add_argument('--urlonly', action='store_true', help='Only print the query URL', dest="urlonly")
    parser.add_argument('-r', '--resource', action='store', type=str,
                        help='Which resource type to use: "intelligence"', dest="resource")
    parser.add_argument('--inteltype', action='store', type=str, help='Intelligence type, comma separated',
                        dest="inteltype")
    parser.add_argument('-s', '--search', action='store', type=str, help='Input search string to look up',
                        dest="search")
    parser.add_argument('-4', '--ipv4', action='store', type=str, help='Provide IPv4 address', dest="input-ipv4")
    parser.add_argument('-6', '--ipv6', action='store', type=str, help='Provide IPv6 address', dest="input-ipv6")
    parser.add_argument('--custom', action='store', type=str, help='Run custom query', dest="custom")
    parser.add_argument('-e', '--enrichmenttype', action='store', type=str,
                        help='Enrichment type "pdns/recorded_future/riskiq_ssl"', dest="enrichmenttype")
    parser.add_argument('--domaininfo', action='store_true', help='Search domain info', dest="domaininfo")
    parser.add_argument('--ipinfo', action='store_true', help='Search IP info', dest="ipinfo")
    parser.add_argument('--examples', action='store_true', help='Show examples', dest="examples")
    parser.add_argument('--intelstatus', action='store', type=str, help='Status active/inactive/falsepos examples',
                        dest="intelstatus")
    parser.add_argument('--sendiocvalue', action='store', type=str,
                        help='Send IoC value', dest="sendiocvalue")
    parser.add_argument('--sendioctype', action='store', type=str,
                        help='Send IoC type "malware, phish"', dest="sendioctype")
    parser.add_argument('--sendiocclassification', action='store', type=str, required=False,
                        help='Send IoC classification, default="private"', dest="sendiocclassification")
    parser.add_argument('--sendiocconfidence', action='store', type=str, required=False,
                        help='Send IoC confidence, default=90', dest="sendiocconfidence")
    parser.add_argument('--sendioctags', action='store', type=str, required=False,
                        help='Send IoC tags, default=\'("bcirt","red"),("phishing","red")\'', dest="sendioctags")
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    # log.info('Usage: {} [query] {ipv4}/{ipv6}')
    args = build_parser()
    resmeta = None
    res = None
    outputtype = None
    # print(args)
    ainteltype = []
    myshowurl = False
    response = "{'Error':'Missing/Wrong arguments!'}"
    if args['urlonly']:
        myshowurl = True
    if args['input-listinteltype']:
        UseAnomali().gettypes()
        exit(0)
    elif args['examples']:
        UseAnomali().showexamples()
        exit(0)
    elif args['resource'] == 'intelligence' and args['search']:
        try:
            if ainteltype:
                ainteltype = str(args['inteltype']).split(',')
            else:
                ainteltype = None
        except Exception:
            print("{'Error':'Wrong intel type'}")
        mystatus = None
        if args['intelstatus'] == 'active' or args['intelstatus'] == 'inactive' or args['intelstatus'] == 'falsepos':
            mystatus = args['intelstatus']
        (resmeta, res) = UseAnomali(showurl=myshowurl).get_intel(papiurl=query_api1_url, papiuser=apiuser,
                                                                 papikey=apikey, pinteltype=ainteltype,
                                                                 psearchvalue=args['search'], pstatus=mystatus)
        outputtype = 'intel'                                                        
        # print("FM:%s FR:%s"%(resmeta, res))
    elif args['sendiocvalue'] and args['sendioctype']:
        asendiocvalue = str(args['sendiocvalue'])
        asendioctype = str(args['sendioctype'])

        # defaults
        asendiocclassification = 'private'
        asendiocconfidence = '90'
        asendioctags = '[{"name":"bcirt","tlp":"red"},{"name":"phishing","tlp":"red"}]'

        try:
            if args['sendiocclassification']:
                asendiocclassification = str(args['sendiocclassification'])
            if args['sendiocconfidence']:
                asendiocconfidence = str(args['sendiocconfidence'])
            if args['sendioctags']:
                asendioctags = str(args['sendioctags'])
                mytags = asendioctags.split(',')
                compiledtag = list()
                for mytag in mytags:
                    tagitem = dict()
                    onetag = mytag.split(':')
                    tagitem['name'] = onetag[0]
                    tagitem['tlp'] = onetag[1]
                    compiledtag.append(tagitem)
                asendioctags = json.dumps(compiledtag)
        except Exception:
            pass
        (resmeta, res) = UseAnomali(showurl=myshowurl).send_ioc(papiurl=query_api1_url, papiuser=apiuser,
                                                                papikey=apikey,
                                                                pthreattype=asendioctype,
                                                                pdatatext=asendiocvalue,
                                                                pclassification=asendiocclassification,
                                                                pconfidence=int(asendiocconfidence),
                                                                ptags=asendioctags
                                                                )
        outputtype = 'iocsubmission'                                                        
    else:
        response = "{'Error':'Missing/Wrong arguments!'}"
        exit(0)
    if args['json']:
        print(resmeta)
        print(res)
    else:
        (outputstr1, outputstr2) = (UseAnomali(showurl=myshowurl).format_output(resmeta, res, outputtype))
        print(outputstr1)
        print(outputstr2)
