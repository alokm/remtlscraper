#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib, urllib2
from BeautifulSoup import BeautifulSoup as soup
from StringIO import StringIO

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
 

    def list(self):
        help = 'list available region codes for scraping'
       
        print "Code | Region Name"
        for region_code, region in sorted(self.region_codes.iteritems()):
            print region_code, region


    def get_region(self, region_code):
        help = 'get specified region code XX as two-digit string for scraper'
    
        headers = { 'User-Agent' : self.user_agent }
        _url = self.url + self.post_url
        self.filename = region_code + '_data.csv'
        
        values = dict()
        values['nom_dossier'] = ''
        values['adress'] = ''
        values['municipalite'] = ''
        values['mrc'] = ''
        values['nom_region'] = region_code
        values['contaminant'] = ''
        encoded = urllib.urlencode(values)   
 
        req = urllib2.Request(_url, data=encoded, headers=headers)
        response = urllib2.urlopen(req)
        page = response.read()
        self.region_page = page.decode('iso-8859-1')


    # read data into outer loop once 
    # parse row into variable in outer loop prior to passing it to the scraper
    # save data.findAll as a variable once per parse row 
    def parse_table(self):
        docsoup = soup(self.region_page)
        table = docsoup.body.findAll('table')
        data = table[4]
        self.tr_data = data.findAll('tr')
        self.num_records = len(self.tr_data)

    def clean_field(self, line):
        if line.find('('):
            openparens = line.find('(')
 	    closeparens = line.find(')')
	    lstring = line[:openparens]
	    raw_mstring = line[openparens:closeparens]
	    clean_mstring = raw_mstring.replace(',','-')
            rstring = line[closeparens:]
	    raw_out = lstring + clean_mstring + rstring
	    clean = raw_out.replace('&nbsp;','')
        else:
	    clean = line.replace('&nbsp;','')
	return clean.replace('\r \n', ' ')

    def parse_field(self, field):
        if field.find(','):
	    fields = field.split(',')
	    cleaned = []
            for field in fields:
	        cleaned.append(self.clean_field(field))
	    return '\n'.join(cleaned)
        else:
            return self.clean_field(field)
	
    def parse_row(self, row):
	tr = self.tr_data
	self.record = dict()
        
	first = tr[row]
        second = tr[row+1]
       
        raw_coords = second.findAll('td')[1].text
        coords = raw_coords.replace(',','.').replace('&nbsp;','')
        raw_adress = first.findAll('td')[1].text.replace('&nbsp;','')
	clean_adress = raw_adress.replace('\r \n', ' ')

	eau = first.findAll('td')[3].text
	cleaned_eau = self.clean_field(eau)
	parsed_eau = self.parse_field(cleaned_eau)

	sol = first.findAll('td')[4].text
	cleaned_sol = self.clean_field(sol)
	parsed_sol = self.parse_field(cleaned_sol)

        self.record['num_fiche'] = second.findAll('td')[0].text
        self.record['lat'] = coords[:coords.find('-')]
        self.record['long'] = coords[coords.find('-'):]
        self.record['nom_dossier'] = first.findAll('td')[0].text
        self.record['adress'] = clean_adress
        self.record['mrc'] = first.findAll('td')[2].text.replace('&nbsp;','')
        self.record['eau_cont'] = parsed_eau
        self.record['sol_cont'] = parsed_sol
	self.record['rehab'] = first.findAll('td')[5].text.split('Q')[0]
        self.parsed_row = [self.record['num_fiche'],
                           self.record['lat'],
                           self.record['long'],
                           self.record['nom_dossier'],
                           self.record['adress'], 
                           self.record['mrc'],
                           self.record['eau_cont'],
                           self.record['sol_cont'],
                           self.record['rehab'],
			   ]
        try:
	    qualite = 'Q' + first.findAll('td')[5].text.split('Q')[1]
	    self.record['qualite'] = qualite
	    self.parsed_row += [self.record['qualite'],]
	except IndexError:
	    print "no info on quality"

      
    def walk_table(self): 
       print '%s records to process' % self.num_records
       filename = 'output/' + self.filename
       savefile = open(filename, 'a')
       for record in range(3, 33, 2):
           raw_row = self.parse_row(record)
	   clean_row = ', '.join(self.parsed_row)
           row = clean_row.encode('iso-8859-1')
           print row
           savefile.write('%s\n' % row)
           print '%s of %s records processed' % (record, self.num_records) 
       savefile.close()
       print 'successfully processed %s records' % self.num_records
