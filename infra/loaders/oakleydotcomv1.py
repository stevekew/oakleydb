import urllib2
from bs4 import BeautifulSoup
from core.archivedotcom import ArchiveDotOrg
from core.logger import Logger
from oakleydb.objectfactory import ObjectFactory
import codecs
import re
import json

# loader constants
LOADER_NAME = 'Oakley.com Loader V1'

# site constants
SITE_URL = 'http://www.oakley.com'
GLASSES_URL = SITE_URL + '/glasses.asp'
LENS_LIST_URL = SITE_URL + '/lens.asp'
GLASSES_MODELS_SUFFIX = 'glassesmodels.asp'
LENS_DETAILS_SUFFIX = 'lensdetail.asp'

# page structure constants
BODYTABLE_CLASS_NAME = 'bodytable'

# generic HTML constants
HTML_COLSPAN_ATTRIBUTE = 'colspan'
HTML_DIV_NODE = 'div'
HTML_CLASS_ATTRIBUTE = 'class'
HTML_TABLE_NODE = 'table'
HTML_LINK_NODE = 'a'
HTML_HREF_ATTRIBUTE = 'href'
HTML_ALT_ATTRIBUTE = 'alt'
HTML_TABLEROW_NODE = 'tr'
HTML_TABLECOL_NODE = 'td'

# BeautifulSoup constants
BS_HTML_PARSER = 'html5lib'
# BS_HTML_PARSER = 'html.parser'


# This loader loads the v1 o-review pages from archive.org
class OakleydotcomV1(object):
    def __init__(self):
        self.logger = Logger(self.__class__.__name__).get()
        self.wayback = ArchiveDotOrg()

    @staticmethod
    def get_name():
        return LOADER_NAME

    def parse_product_details(self, node):

        details = {}
        for item in node.find_all('li'):
            name = item.find('span', {'class': 'product-info-title'}).string
            val = item.find('span', {'class': 'product-info-value'}).string
            details[name] = val

        return details

    def load_from_file(self, filename):
        html_file = codecs.open(filename, 'r')

        html_doc = html_file.read()

        soup = BeautifulSoup(html_doc, BS_HTML_PARSER)

        product_script = soup.find_all('script', text=re.compile(r'var utag_data ='))

        product_details = soup.find('div', {'class': 'product-attributes'})

        product_details = product_details.find('ul', {'class': 'product-info'})

        details = self.parse_product_details(product_details)

        text = product_script[0].string
        text = text.replace('var utag_data =', '')

        json_data = json.loads(text)

        details['List Price'] = json_data['product_list_price'][0]
        details['Name'] = json_data['product_name'][0].replace('&trade;', '')
        details['SKU'] = json_data['product_sku'][0]

        # categories
        category_script = soup.find_all('script', text=re.compile(r'categoryName.push'))
        category_text = category_script[0].string

        categories = re.findall('categoryName.push\("(.+?)"\)', category_text)

        # 'New Sunglasses'
        print details

loader = OakleydotcomV1()

loader.load_from_file('/home/pi/Projects/oakleydb/cp/Oakley Carbon Prime MotoGP Limited Edition.html')
