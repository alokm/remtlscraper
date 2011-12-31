import unittest
from urllib import urlopen
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup as soup

class TestBaseScraper(unittest.TestCase):
    def setUp(self):
        self.base_url = u'http://www.mddep.gouv.qc.ca/sol/terrains/terrains-contamines/recherche.asp'
	self.test_text = open('tests/fixtures/testfile.html', 'r').readlines()
	self.parsed_file = soup(StringIO(self.test_text))

    def test_parse_page_file(self):
	nom_text_file = self.parsed_file.html.body.findAll('p')[3].text[:14]
        self.assertEqual(nom_text_file, u'Nom du dossier')

    def tearDown(self):
	pass

if __name__ == '__main__':
    unittest.main()
