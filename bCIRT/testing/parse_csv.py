#!/usr/env/python
# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : accounts/admin.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Admin file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
import argparse
import csv

class parse_exchange_report():
    def __init__(self, pfile):
        try:
            with open(pfile) as f:
                reader = csv.DictReader(f)
                self.dataCSV = [r for r in reader]
                # self.row_count = sum(1 for row in csvfile)
                # self.readCSV = csv.reader(csvfile, delimiter=',')
                # colnum = len(next(readCSV))

        except Exception:
            print("File cannot be read: %s"%(pfile))
            exit(1)

    def list_recipients(self):
        res = set()
        for row in self.dataCSV:
            res.add(row['Location Name'])
        return res

    def print_csvstats(self):
        rownum = len(self.dataCSV)
        colnum = len(self.dataCSV[0])
        return (colnum,rownum)

def build_parser():
    parser = argparse.ArgumentParser(description='Parse Exchange Report.', usage='parse_exchange_report [options]')
    parser.add_argument("file", help="File to read - CSV format")
    # parser.add_argument('-o', '--outfile', action='store', type=str, help='Save output file full path', dest="save-outfile-to")
    parser.add_argument('-c', '--csvstats', action='store_true', help='Print CSV statistics', dest="csvstats")
    parser.add_argument('-l', '--listrecipients', action='store_true', help='Print recipient list', dest="listrecipients")
    args = vars(parser.parse_args())
    return args

if __name__ == "__main__":
    args = build_parser()
    # print(args)

    if args['file'] and args['csvstats']:
        res = parse_exchange_report(pfile=args['file']).print_csvstats()
        print("Columns:%s\nRows:%d"%(res[0],res[1]))
    if args['file'] and args['listrecipients']:
        res = parse_exchange_report(pfile=args['file']).list_recipients()
        for item in res:
            print(item)
