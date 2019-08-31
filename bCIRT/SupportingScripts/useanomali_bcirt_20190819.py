#!/usr/bin/python3
# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : scripts/useanomali_bcirt_20190818.py
# Author            : Balazs Lendvay
# Date created      : 2019.08.18
# Purpose           : Anomali query script for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.08.18  Lendvay     1      Initial file
# **********************************************************************;

import requests
import logging as log
from sys import exit
from collections.abc import Iterable
import argparse
import os

apiuser = ''
apikey = ''
query_api1_url = 'https://api.threatstream.com/api/v1'
query_api2_url = 'https://api.threatstream.com/api/v2'
# test values '4DA1F312A214C07143ABEEAFB695D904' mal_md5
# 179.61.149.247 bot_ip
# www.ifferfsodp9ifjaposdfjhgosurijfaewrwergwea.com
# log.basicConfig(format='%(message)s', level=log.INFO)
#/api/v1/impact

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
            'python3 useunomali.py -e pdns --ipinfo -s 195.22.26.248\n',
            'python3 useunomali.py -e pdns --domaininfo -s www.ifferfsodp9ifjaposdfjhgosurijfaewrwergwea.com\n',
            "python3 useunomali.py --custom 'limit=3' --resource threat_model_search\n",
            "python3 useanomali.py --resource intelligence --custom '&value__contains=179.61.149.247&limit=3&status="
            "active&extend_source=true&itype=bot_ip'\n",
        ]

    def gettypes(self, filter=None):
        for item in self.itypes:
            print(item)


    def showexamples(self):
        for item in self.examples:
            print(item)


    # https://api.threatstream.com/api/v1/threat_model_search/&limit=100
    def query_api(self, papiurl, papiuser, papikey, presource, pflags='',pjsonobjname='objects'):
        http_outcode = None
        url = '{}/{}/?username={}&api_key={}{}'.format(papiurl, presource, papiuser, papikey, pflags)
        if self.showurl:
            print(url)
            exit(0)
        try:
            http_req = requests.get(url, headers={'ACCEPT': 'application/json, text/html'})
            if http_req.status_code == 200:
                return (http_req.json()[pjsonobjname])  # Return JSON Blob
                # return (http_req.json()['objects'])  # Return JSON Blob
            elif http_req.status_code == 401:
                log.error('Access Denied. Check API Credentials')
                exit(0)
            else:
                log.info('API Connection Failure. Status code: {}'.format(http_req.status_code))
        except Exception as err:
            log.error('API Access Error: {}'.format(err))
            exit(0)

    def get_custom(self, papiurl, papiuser, papikey, presource, pcustom):
        r = []
        log.info('Running Custom query: \n')
        pflags = ''
        if pcustom:
            pflags = '{}&{}'.format(pflags, pcustom)
            res = self.query_api(papiurl, papiuser, papikey, presource, pflags)
            if res:
                if res[0]:
                    r.append(res[0])
                # else:
                #     r = {'Result': 'No Data'}
            # else:
            #     r = {'Result': 'No Data'}
        else:
            r = {'Result': 'No Data'}
        return (r)

    def get_intel(self, papiurl, papiuser, papikey, pinteltype=None, psearchvalue=None,
                  psearchregex=False, psearchregexp=False, psearchcontains=False,
                  psearchexact=False, psearchstartswith=False,
                  plimit=3, pstatus='active',
                  pextend_source=True):
        r = []
        log.info('Downloading intelligence: \n')
        # INTEL = {'c2_domain', 'bot_ip'}  # filter to itype
        pflags = ''
        if not psearchregex and not psearchregexp and not psearchcontains and not psearchexact and not psearchstartswith:
            psearchcontains=True
        if psearchregex and psearchvalue:
            pflags = '{}&value__regex={}'.format(pflags,psearchvalue)
        elif psearchregexp and psearchvalue:
            pflags = '{}&value__regexp={}'.format(pflags,psearchvalue)
        elif psearchcontains and psearchvalue:
            pflags = '{}&value__contains={}'.format(pflags,psearchvalue)
        elif psearchstartswith and psearchvalue:
            pflags = '{}&value__startswith={}'.format(pflags,psearchvalue)
        elif psearchexact and psearchvalue:
            pflags = '{}&value={}'.format(pflags,psearchvalue)
        if plimit:
            pflags = '{}&limit={}'.format(pflags,plimit)
        if pstatus:
            pflags = '{}&status={}'.format(pflags,pstatus)
        if pextend_source:
            pflags = '{}&extend_source=true'.format(pflags)
        else:
            pflags = '{}&extend_source=false'.format(pflags)
        if isinstance(pinteltype, Iterable):
            for itype in pinteltype:
                pflagstmp = '{}&itype={}'.format(pflags, itype)
                res = self.query_api(papiurl=papiurl, papiuser=papiuser, papikey=papikey, presource='intelligence', pflags=pflagstmp, pjsonobjname='objects')
                if len(res)>0:
                    r.append(res[0])
        else:
            res = self.query_api(papiurl=papiurl, papiuser=papiuser, papikey=papikey, presource='intelligence', pflags=pflags, pjsonobjname='objects')
            if len(res)>0:
                r.append(res[0])
            #r = {'Result': 'No Data'}
        # print("R:%s"%(r))
        return (r)

    def get_enrichment(self, papiurl, papiuser, papikey, psearchvalue, penrichmenttype, ptype):
        r = []
        log.info('Downloading intelligence: \n')
        # INTEL = {'c2_domain', 'bot_ip'}  # filter to itype
        if penrichmenttype == 'pdns':
            if ptype == "domaininfo":
                penrichmenttype = 'pdns/domain/{}'.format(psearchvalue)
            elif ptype == "ipinfo":
                penrichmenttype = 'pdns/ip/{}'.format(psearchvalue)
            else:
                r = {'Result': 'Wrong parameters'}
            res = self.query_api(papiurl, papiuser, papikey, penrichmenttype, pflags='', pjsonobjname='results')
            if res:
                if len(res)>0:
                    # print("RES:%s"%(res))
                    r.append(res[0])
            else:
                r = {'Result': 'Missing parameter'}
        else:
            r = {'Result': 'Missing parameter'}
        # print("R:%s"%(r))
        return (r)

    def format_output(self, jsonblob):
        r = ""
        if jsonblob and isinstance(jsonblob,list):
            # print("JSON:%s"%(jsonblob))
            # r += "'Success': '{}'".format(self.issuccess)
            for line in jsonblob:
                # print("LINE:%s"%(line))
                for k, v in line.items():
                    if not v: continue
                    r += "{}: {}\n".format(k, v)
        else:
           r = {'Result':'Not parsable Data or No data'}
        return (r)


def build_parser():
    parser = argparse.ArgumentParser(description='Use Anomali', usage='useanomali [options]')
    # parser.add_argument("input", help="Search term to look for")
    parser.add_argument('-t', '--listinteltypes', action='store_true', help='List intelligence types',
                        dest="input-listinteltype")
    parser.add_argument('-j', '--json', action='store_true', help='Output in JSON', dest="json")
    parser.add_argument('--urlonly', action='store_true', help='Only print the query URL', dest="urlonly")
    parser.add_argument('-r', '--resource', action='store', type=str, help='Which resource type to use: "intelligence"', dest="resource")
    parser.add_argument('--inteltype', action='store',type=str, help='Intelligence type, comma separated', dest="inteltype")
    parser.add_argument('-s', '--search', action='store', type=str, help='Input search string to look up', dest="search")
    parser.add_argument('-4', '--ipv4', action='store', type=str, help='Provide IPv4 address', dest="input-ipv4")
    parser.add_argument('-6', '--ipv6', action='store', type=str, help='Provide IPv6 address', dest="input-ipv6")
    parser.add_argument('--custom', action='store', type=str, help='Run custom query', dest="custom")
    parser.add_argument('-e','--enrichmenttype', action='store', type=str,
                        help='Enrichment type "pdns/recorded_future/riskiq_ssl"', dest="enrichmenttype")
    parser.add_argument('--domaininfo', action='store_true', help='Search domain info', dest="domaininfo")
    parser.add_argument('--ipinfo', action='store_true', help='Search IP info', dest="ipinfo")
    parser.add_argument('--examples', action='store_true', help='Show examples', dest="examples")



    args = vars(parser.parse_args())
    return args

if __name__ == "__main__":
    log.info('Usage: {} [query] {ipv4}/{ipv6}')
    args = build_parser()
    # print(args)
    ainteltype = []
    myshowurl = False
    response="{'Error':'Missing/Wrong arguments!'}"
    if args['urlonly']:
        myshowurl = True
    if args['input-listinteltype']:
        UseAnomali().gettypes()
        exit(0)
    elif args['examples']:
        UseAnomali().showexamples()
        exit(0)
    elif args['enrichmenttype'] and (args['domaininfo'] or args['ipinfo']):
        atype=None
        if args['domaininfo']:
            atype = "domaininfo"
        elif args['ipinfo']:
            atype = "ipinfo"
        response = UseAnomali(showurl=myshowurl).get_enrichment(papiurl=query_api1_url, papiuser=apiuser, papikey=apikey,
                                    psearchvalue=args['search'], penrichmenttype=args['enrichmenttype'],
                                    ptype=atype)
    elif args['custom'] and args['resource']:
        response = UseAnomali(showurl=myshowurl).get_custom(papiurl=query_api1_url, papiuser=apiuser, papikey=apikey,
                                           presource=args['resource'], pcustom=args['custom'])
    elif args['resource']=='intelligence' and args['search']:
        try:
            if ainteltype:
                ainteltype = str(args['inteltype']).split(',')
            else:
                ainteltype = None
        except Exception:
            print("{'Error':'Wrong intel type'}")
        response = UseAnomali(showurl=myshowurl).get_intel(papiurl=query_api1_url, papiuser=apiuser, papikey=apikey,
                             pinteltype=ainteltype, psearchvalue=args['search'])
    else:
        response="{'Error':'Missing/Wrong arguments!'}"
        exit(0)
    if args['json']:
        print(response)
    else:
        print(UseAnomali(showurl=myshowurl).format_output(response))  ## Make human readable.
