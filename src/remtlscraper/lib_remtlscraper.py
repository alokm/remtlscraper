#!/usr/bin/python

from urllib import urlopen
from BeautifulSoup import BeautifulSoup as soup
#from lxml import etree


class BaseScraper(object):
    help = 'Command line utility to mine data for ReMtl.ca'

    def __init__(self):
        self.url = "http://www.mddep.gouv.qc.ca/sol/terrains/terrains-contamines/recherche.asp"
        self.page = urlopen(self.url)
        self.text = self.page.read()
        self.doc = soup(self.text)
        self.form = self.doc.body.find('form')
        self.table = self.form.find('table')
        self.rows = self.table.findAll('tr') 
        self.muni = self.rows[3]
        self.mrc = self.rows[4]
        self.cont = self.rows[5]

    def update_codes(self):
        print "Retrieving Municipality Codes"

        municipalite = dict()
        for item in self.muni.findAll('option'):
            if item.text == 'Tous':
                print '-' * 40
                print u'Code| Municipalite'
                print '-' * 40
            else:
                municipalite[item.attrs[0][1]] = item.text
                print item.attrs[0][1] + ' | ' + item.text
    
        # next step: modify update_codes method to return munis
        # as dict() with codes as keys and muni name as value
        
        # To do: add mrc and contaminant updaters
        #   mrc = dict()
        #   contaminant = dict()

if '__name__' == '__main__':
    scraper = BaseScraper()
    scraper.update_codes()
