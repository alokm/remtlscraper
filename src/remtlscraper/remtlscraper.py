#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import lib

parser = argparse.ArgumentParser()

title="Command line utility for downloading pdf docs on contamination data"

parser = argparse.ArgumentParser(description=title)
parser.add_argument('-g', action='store', metavar='MRC',
                    dest='mrc_code',
                    help='MRC code for region or municipality')
parser.add_argument('-l', '--list', action='store_true', default=False,
                    dest='listflag',
                    help='list available MRC codes')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0',
                    help='last updated 2011-12-23 by Alok Mohindra')

results = parser.parse_args()

scraper = lib.BaseScraper()
if results.listflag == True:
    print 'list of mrc codes:'
    scraper.list() 
elif results.mrc_code is not None:
    print 'user specified the following codes:'
    print results.mrc_code
    print '-' * 20
    print 'pass lib.py the following codes' 
    scraper.get_region(results.mrc_code)
    scraper.parse_region_table(3)
    #scraper.walk_region_table()
    print 'success!' 
else:
    print """usage: remtlscraper.py [-h] [-g MRC] [-l] [-v]

Command line utility for downloading pdf docs on contamination data

optional arguments:
  -h, --help     show this help message and exit
  -g MRC         MRC code for region or municipality
  -l, --list     list available MRC codes
  -v, --version  last updated 2011-12-23 by Alok Mohindra
""" 
