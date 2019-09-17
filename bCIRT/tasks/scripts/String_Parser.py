# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : tasks/scripts/StringParser.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Internal command actions file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
import re
import ipaddress

class StringParser():
    def find_ipv4(self, str1):
        ipattern = re.compile(
            '(?:(?:1\d\d|2[0-5][0-5]|2[0-4]\d|0?[1-9]\d|0?0?\d)\.){3}(?:1\d\d|2[0-5][0-5]|2[0-4]\d|0?[1-9]\d|0?0?\d)')
        imatches = re.findall(ipattern, str1)
        imatches = sorted(list(set(imatches)))
        return imatches

    def find_ipv6(self, str1):
        ipattern = re.compile('(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}')
        imatches = re.findall(ipattern, str1)
        imatches = sorted(list(set(imatches)))
        return imatches

    def ip_check(self, address):
        try:
            ipver = ipaddress.ip_address(address)
            return ipver
        except:
            return False

    def find_email(self, str1):
        #  ipattern = re.compile('([^[({@|\s]+@[^@]+\.[^])}@|\s]+)')
        ipattern = re.compile('([^@":[>|<\s]+@[^@]+\.[^]>"<)\}@|\s]+)')
        imatches = re.findall(ipattern, str1)
        imatches = sorted(list(set(imatches)))
        return imatches

    def extract_ip(self, str1):
        ip4 = None
        ip6 = None
        ip4 = self.find_ipv4(str1)
        ip6 = self.find_ipv6(str1)
        return ip4.append(ip6)

    def extract_email(self, str1):
        emails = []
        emails = self.find_email(str1)
        return emails

    def extract_all(self):
        self.extract_email()
        self.extract_ip()

    def check_malicious(self, str1):
        str1 = str1.lower()
        ipatternU = re.compile(r'\'malicious\':\W+\'unknown\'')
        ipatternC = re.compile(r'\'malicious\':\W+\'clean\'')
        ipatternS = re.compile(r'\'malicious\':\W+\'suspicious\'')
        ipatternM = re.compile(r'\'malicious\':\W*\'malicious\'')
        if bool(re.search(ipatternU, str1)):
            imatches = 'Unknown'
        elif bool(re.search(ipatternC, str1)):
            imatches = 'Clean'
        elif bool(re.search(ipatternS, str1)):
            imatches = 'Suspicious'
        elif bool(re.search(ipatternM, str1)):
            imatches = 'Malicious'
        else:
            imatches = "Unknown"
        return imatches
