import urllib2
from bs4 import BeautifulSoup
from core.archivedotcom import ArchiveDotOrg
from core.logger import Logger

# loader constants
LOADER_NAME = 'O-Review Loader V1'

# site constants
SITE_URL = 'http://www.o-review.com'
GLASSES_URL = SITE_URL + '/glasses.asp'
GLASSES_MODELS_SUFFIX = 'glassesmodels.asp'

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
BS_HTML_PARSER = 'html.parser'


# This loader loads the v1 o-review pages from archive.org
class OReviewLoaderV1(object):

    def __init__(self):
        self.logger = Logger(self.__class__.__name__).get()
        self.wayback = ArchiveDotOrg()

    @staticmethod
    def get_name():
        return LOADER_NAME

    def get_family_list(self):
        return self.parse_glasses_list_page_families(GLASSES_URL)

    def get_style_list(self):
        return self.parse_glasses_list_page_styles(GLASSES_URL)

    def get_models_for_style(self, style_name, url):
        return self.parse_models_page(style_name, url)

    def get_oreview_body_div(self, url):
        #  use the wayback api to work out the best cached copy for this page
        archive_url = self.wayback.find_archive_url(url)
        self.logger.info("Found archive URL: [{}]".format(archive_url))

        response = urllib2.urlopen(archive_url)

        html_doc = response.read()

        self.logger.debug(html_doc)

        soup = BeautifulSoup(html_doc, BS_HTML_PARSER)

        # find the fiv that holds the details table
        div = soup.body.find(HTML_DIV_NODE, attrs={HTML_CLASS_ATTRIBUTE: BODYTABLE_CLASS_NAME})

        return div

    def get_oreview_data_table(self, url):

        # get the main body div that contains the table
        div = self.get_oreview_body_div(url)

        # get the table
        table = div.find(HTML_TABLE_NODE)

        return table

    def parse_glasses_list_page_families(self, url):
        table = self.get_oreview_data_table(url)

        # select out all the rows
        rows = table.find_all(HTML_TABLEROW_NODE)

        self.logger.info("Table contains [{}] rows".format(len(rows)))

        families = []
        for row in rows:
            if row.contents[0].name == HTML_TABLECOL_NODE:
                cell = row.td
                # if the cell has a colspan attribute it contains the collection/range
                if HTML_COLSPAN_ATTRIBUTE in cell.attrs:
                    family = unicode(row.td.b.string)
                    self.logger.debug("Processed family: [{}]".format(family))

                    families.append(family)

        return families

    def parse_glasses_list_page_styles(self, url):
        table = self.get_oreview_data_table(url)

        # select out all the rows
        rows = table.find_all(HTML_TABLEROW_NODE)

        self.logger.info("Table contains [{}] rows".format(len(rows)))

        styles = []
        family = ''
        for row in rows:
            if row.contents[0].name == HTML_TABLECOL_NODE:
                cell = row.td
                # if the cell has a colspan attribute it contains the collection/range
                if HTML_COLSPAN_ATTRIBUTE in cell.attrs:
                    family = unicode(row.td.b.string)
                    self.logger.debug("Processed family: [{}]".format(family))
                elif cell.contents[0].name == HTML_LINK_NODE:
                    link = cell.a

                    if HTML_HREF_ATTRIBUTE in link.attrs:
                        if link[HTML_HREF_ATTRIBUTE].startswith(GLASSES_MODELS_SUFFIX):
                            models_url = SITE_URL + '/' + link[HTML_HREF_ATTRIBUTE]

                            item = {'name': unicode(link.string), 'family': unicode(family), 'url': models_url}

                            self.logger.debug(unicode("[{}]: [{}]").format(item['name'], item['url']))

                            styles.append(item)

        return styles

    def parse_models_page(self, style_name, url):
        table = self.get_oreview_data_table(url)

        if table is None:
            self.logger.error('Failed to find a data table for url [{}]'.format(url))
            return {}

        table = table.find(HTML_TABLE_NODE)

        rows = table.find_all(HTML_TABLEROW_NODE)

        models = []
        for row in rows:
            model = {}
            cols = row.find_all(HTML_TABLECOL_NODE)
            name = ''
            if cols[1].a is not None:
                name = cols[1].a.string

            if unicode(name) == '':
                self.logger.error('No model name found for row [{}]'.format(row))
                continue

            model['name'] = '{} {}'.format(style_name, unicode(name))
            model['listprice'] = unicode(cols[2].string)
            model_url = SITE_URL + '/' + cols[1].a[HTML_HREF_ATTRIBUTE]
            model['url'] = unicode(model_url)

            sku = ''
            if cols[3].font is not None:
                sku = str(cols[3].font.string)
                sku = str.replace(sku, '[', '')
                sku = str.replace(sku, ']', '')

            model['sku'] = unicode(sku)

            models.append(model)

        return models
