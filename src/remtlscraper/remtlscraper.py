#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import lib

def scraper(inputs):
    scraper = lib.BaseScraper()
    if inputs.listflag == True:
        print 'list of region codes:'
        scraper.list() 
    elif inputs.region_code is not None:
        print 'user specified the following region codes:'
        print inputs.region_code
        print '-' * 20
        print 'pass lib.py the following codes' 
        scraper.get_region(inputs.region_code)
	scraper.parse_region_table(3)
        scraper.walk_region_table()
        print 'success!' 
    else:
        print """To retrieve data for a region enter the following from the command line to retrieve data for region 06 = Montreal

$ python remtlscraper.py -g 06 
"""

parser = argparse.ArgumentParser()

title="Command line utility for downloading pdf docs on contamination data"

parser = argparse.ArgumentParser(description=title)
parser.add_argument('-g', action='store', metavar='Region',
                    dest='region_code',
                    help='Region code for region or municipality')
parser.add_argument('-l', '--list', action='store_true', default=False,
                    dest='listflag',
                    help='list available region codes')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0',
                    help='last updated 2011-12-23 by Alok Mohindra')

results = parser.parse_args()

get_results = scraper(results)
