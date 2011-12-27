#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2
from BeautifulSoup import BeautifulSoup as soup


class BaseScraper(object):
    help = 'Command line utility to mine data for ReMtl.ca'

    def __init__(self):
        self.url = "http://www.mddep.gouv.qc.ca/sol/terrains/terrains-contamines/"
        self.get_url = "recherche.asp"
        self.post_url = "resultats.asp"
        
        self.user_agent = 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1' 
 
        self.region_codes = { "99" : u"Tous",
                           "08" : u"Abitibi-Témiscamingue",
                           "01" : u"Bas-Saint-Laurent",
                           "03" : u"Capitale-Nationale",
                           "17" : u"Centre-du-Québec",
                           "12" : u"Chaudière-Appalaches",
                           "09" : u"Côte-Nord",
                           "05" : u"Estrie",
                           "11" : u"Gaspésie--Îles-de-la-Madeleine",
                           "14" : u"Lanaudière",
                           "15" : u"Laurentides",
                           "13" : u"Laval",
                           "04" : u"Mauricie",
                           "16" : u"Montérégie",
                           "06" : u"Montréal",
                           "10" : u"Nord-du-Québec",
                           "07" : u"Outaouais",
                           "02" : u"Saguenay--Lac-Saint-Jean", }
 

    def get_region(self, region_code):
        headers = { 'User-Agent' : self.user_agent }
        _url = self.url + self.post_url
        
        values = dict()
        values['nom_dossier'] = ''
        values['adress'] = ''
        values['municipalite'] = ''
        values['mrc'] = ''
        values['nom_region'] = region_code
        values['contaminant'] = ''
        encoded = urllib.urlencode(values)   
 
        print 'retrieving data for: %s' % encoded
        req = urllib2.Request(_url, data=encoded, headers=headers)
        response = urllib2.urlopen(req)
        self.region_page = response.read()
        return self.region_page
        print self.region_page


    def list(self):
        print "Code | MRC"
        for region_code, region in sorted(self.region_codes.iteritems()):
            print region_code, region


    def parse_region_table(self, row):
        docsoup = soup(self.region_page)
        table = docsoup.body.findAll('table')
        data = table[4]
        self.num_records = len(data.findAll('tr'))
        coords = data.findAll('tr')[row+1].findAll('td')[1].text

        self.record = dict()
        self.record['num_fiche'] = data.findAll('tr')[row+1].findAll('td')[0].text
        self.record['lat'] = coords[:coords.find('-')]
        self.record['long'] = coords[coords.find('-'):]      
        self.record['nom_dossier'] = data.findAll('tr')[row].findAll('td')[0].text
        self.record['adress'] = data.findAll('tr')[row].findAll('td')[1].text
        self.record['mrc'] = data.findAll('tr')[row].findAll('td')[2].text
        self.record['eau_cont'] = data.findAll('tr')[row].findAll('td')[3].text
        self.record['sol_cont'] = data.findAll('tr')[row].findAll('td')[4].text
        self.record['etat_rehab'] = data.findAll('tr')[row].findAll('td')[5].text
        parsed_row = [self.record['num_fiche'],
                      self.record['lat'],
                      self.record['long'],
                      self.record['nom_dossier'],
                      self.record['adress'], self.record['mrc'],
                      self.record['eau_cont'],
                      self.record['sol_cont'],
                      self.record['etat_rehab']]
        return parsed_row
        
        
    def walk_region_table(self):
       print '%s records to process' % self.num_records 
       for record in range(3, self.num_records, 2):
           row = ','.join(self.parse_region_table(record)).encode('utf8')
           savefile = open('savefile.csv', 'w')
           savefile.write(row)
           print row
           print '%s of %s records processed' % (record, self.num_records) 
       savefile.close()
       print 'successfully processed %s records' % self.num_records

    def save(self):
        titles = u'Numéro de la fiche,Coordinées,Nature des Contaminants (Sol Souterraine)' + \
        'État de la réhabilitation (R)\n Qualité des sols résiduels après réhabilitation (Q)'

        self.savefile = open('savefile.html', 'w')
        self.savefile.write(self.region_page)
        self.savefile.close()
        print 'wrote savefile'
