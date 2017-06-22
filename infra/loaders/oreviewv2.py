import urllib2
from bs4 import BeautifulSoup
from core.archivedotcom import ArchiveDotOrg
from core.logger import Logger
from oakleydb.objectfactory import ObjectFactory

# loader constants
LOADER_NAME = 'O-Review Loader V2'

# site constants
SITE_URL = 'http://www.o-review.com'
DATABASE_URL = SITE_URL + '/database_timeline.php'

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


# This loader loads the v2 o-review pages from archive.org
class OReviewLoaderV2(object):
    def __init__(self):
        self.logger = Logger(self.__class__.__name__).get()
        self.wayback = ArchiveDotOrg()

    @staticmethod
    def get_name():
        return LOADER_NAME

    def get_style_list(self):
        return self.parse_database_list_page(DATABASE_URL)

    def parse_database_list_page(self, url):
        print 'parse'
