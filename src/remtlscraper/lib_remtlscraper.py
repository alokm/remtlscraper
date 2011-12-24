#!/usr/bin/python

from urllib import urlopen
from BeautifulSoup import BeautifulSoup as soup


class BaseScraper(object):
    help = 'Command line utility to mine data for ReMtl.ca'

    def __init__(self):
        self.url = "http://www.mddep.gouv.qc.ca/sol/terrains/terrains-contamines/recherche.asp"
        self.page = urlopen(self.url)

    def retrieve_content(self):
        self.text = self.page.read()
        self.doc = soup(self.text)
        self.form = self.doc.body.find('form')
        self.table = self.form.find('table')
        self.rows = self.table.findAll('tr') 
        self.mrc = self.rows[4]
        self.cont = self.rows[5]


    def update_codes(self):
        print "Retrieving Municipality Codes"

        self.mrc_code = dict()
        for item in self.mrc.findAll('option'):
            if item.text == 'Tous':
                print '-' * 40
                print u'Code| MRC'
                print '-' * 40
            else:
                self.mrc_code[item.attrs[0][1]] = item.text
                print item.attrs[0][1] + ' | ' + item.text
    
    def list_codes(self):
        del self.mrc_code['99']
        print u'Code| MRC'
        for k, v in sorted(self.mrc_code.iteritems()):
                print k, v

    def get_codes(self):
        pass

if '__name__' == '__main__':
    scraper = BaseScraper()
    scraper.update_codes()
