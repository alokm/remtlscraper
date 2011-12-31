#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from urllib import urlopen
import urllib, urllib2
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup as soup

class TestBaseScraper(unittest.TestCase):
    def setUp(self):
        self.url = "http://www.mddep.gouv.qc.ca/sol/terrains/terrains-contamines/"
        self.get_url = "recherche.asp"
        self.post_url = "resultats.asp"
        self.user_agent = 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1' 
        self.region_codes = { "01" : u"Bas-Saint-Laurent",
                              "06" : u"Montréal", }

    def test_get_url(self):
        headers = { 'User-Agent' : self.user_agent }
        _url = self.url + self.get_url
	self.assertEqual(_url[:27], 'http://www.mddep.gouv.qc.ca')
	self.assertEqual(self.post_url, 'resultats.asp')

    def test_region_code(self):
        self.assertEqual(self.region_codes['01'], u'Bas-Saint-Laurent')

    def test_region_unicode(self):
        code = self.region_codes['06']
        self.assertEqual(code, u'Montréal')
        self.assertEqual(ord(code[5]), 233) # check for e accent egu as unicode#
