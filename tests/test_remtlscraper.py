import unittest
from urllib import urlopen

class TestBaseScraper(unittest.TestCase):
    def setUp(self):
        self.base_url = u'http://www.mddep.gouv.qc.ca/sol/terrains/terrains-contamines/recherche.asp'
        self.page = urlopen(self.base_url)
        self.text = self.page.read()

    def test_url_opens_page(self):
        self.assertEqual(self.page.code, 200)

    def test_read_page(self):
        return 0

if __name__ == '__main__':
    unittest.main()
