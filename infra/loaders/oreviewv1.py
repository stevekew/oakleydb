import urllib2
from bs4 import BeautifulSoup
from core.archivedotcom import ArchiveDotOrg
from core.logger import Logger
from oakleydb.objectfactory import ObjectFactory

# loader constants
LOADER_NAME = 'O-Review Loader V1'

# site constants
SITE_URL = 'http://www.o-review.com'
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

    def get_model_details(self, model):
        return OReviewLoaderV1.convert_to_oakleydb_model_details(model, self.parse_details_page(model['url']))

    def get_lens_list(self):
        return self.parse_lens_list_page(LENS_LIST_URL)

    def get_lens_details(self, lens):
        return OReviewLoaderV1.convert_to_oakleydb_lens_details(lens, self.parse_details_page(lens['url']))

    def get_oreview_body_div(self, url):
        #  use the wayback api to work out the best cached copy for this page
        archive_url = self.wayback.find_archive_url(url)

        if archive_url is None:
            self.logger.error("Found no archive URL for: [{}]".format(url))
            return None

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

        if div is None:
            return None

        # get the table
        table = div.find(HTML_TABLE_NODE)

        return table

    def parse_glasses_list_page_families(self, url):
        table = self.get_oreview_data_table(url)

        if table is None:
            self.logger.error('Failed to find a data table for url [{}]'.format(url))
            return {}

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

        if table is None:
            self.logger.error('Failed to find a data table for list page with url [{}]'.format(url))
            return {}

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
            self.logger.error('Failed to find a data table for models page with url [{}]'.format(url))
            return {}

        table = table.find(HTML_TABLE_NODE)

        rows = table.find_all(HTML_TABLEROW_NODE)

        models = []
        for row in rows:
            cols = row.find_all(HTML_TABLECOL_NODE)
            name = ''
            if cols[1].a is not None:
                name = cols[1].a.string

            if unicode(name) == '':
                self.logger.error('No model name found for row [{}]. Skipping...'.format(row))
                continue

            model_url = SITE_URL + '/' + cols[1].a[HTML_HREF_ATTRIBUTE]

            model = {'name': unicode(name), 'listprice': unicode(cols[2].string),
                     'url': unicode(model_url), 'style': style_name}

            sku = ''
            if cols[3].font is not None:
                sku = str(cols[3].font.string)
                sku = str.replace(sku, '[', '')
                sku = str.replace(sku, ']', '')

            model['sku'] = unicode(sku)

            # model_details = self.parse_details_page(model_url)
            #
            # # confirm the SKUs match before processing
            # process_details = False
            # if 'SKU#' in model_details:
            #     if model['sku'] == model_details['SKU#']:
            #         process_details = True
            #     else:
            #         self.logger.error(
            #             "SKU for model [{}] ([{}]) does not match SKU for model details [{}]. Not processing model details".
            #                 format(model['name'], model['sku'], model['SKU#']))
            # else:
            #     self.logger.error("No SKU found for model details page with URL [{}]".format(model['url']))

            # if process_details:
            #     if 'Frame' in model_details:
            #         model['frame'] = model_details['Frame']
            #     if 'Lens' in model_details:
            #         model['lens'] = model_details['Lens']
            #     if 'Release Date' in model_details:
            #         model['releasedate'] = model_details['Release Date']
            #     if 'Retire Date' in model_details:
            #         model['retiredate'] = model_details['Retire Date']
            #     # if '' in model_details: model[''] = model_details['Model']
            #     # if '' in model_details: model[''] = model_details['SKU#']
            #     # if '' in model_details: model[''] = model_details['UPC']
            #     # if '' in model_details: model[''] = model_details['USD']
            # else:
            #     model['frame'] = ''
            #     model['lens'] = ''
            #     model['releasedate'] = ''
            #     model['retiredate'] = ''

            models.append(model)

        return models

    def parse_details_page(self, url):
        body_table = self.get_oreview_data_table(url)

        if body_table is None:
            self.logger.error('Failed to find a data table for frame details page with url [{}]'.format(url))
            return {}

        table = body_table.find(HTML_TABLE_NODE)

        if table is None:
            table = body_table

        # print table
        rows = table.find_all(HTML_TABLEROW_NODE)

        details = {}
        for row in rows:
            cols = row.find_all(HTML_TABLECOL_NODE)

            # only take rows with a key and value column
            if len(cols) == 2:
                if cols[1].string is not None:
                    details[unicode(cols[0].string)] = unicode(cols[1].string)

        return details

    def parse_lens_list_page(self, url):
        table = self.get_oreview_data_table(url)

        if table is None:
            self.logger.error('Failed to find a data table for lens list page with url [{}]'.format(url))
            return {}

        # select out all the rows
        rows = table.find_all(HTML_TABLEROW_NODE)

        self.logger.info("Table contains [{}] rows".format(len(rows)))

        lenses = []
        lens_type = ''
        count = -1
        for row in rows:
            count += 1

            # skip the first row
            if count == 0:
                continue

            cells = row.find_all(HTML_TABLECOL_NODE)

            if len(cells) == 1:
                # category
                lens_type = unicode(cells[0].text)
            else:
                lens_url = ''
                # if cell 0 is the one with the link and the name
                if cells[0].contents[0].name == HTML_LINK_NODE:
                    link = cells[0].a

                    if HTML_HREF_ATTRIBUTE in link.attrs:
                        if link[HTML_HREF_ATTRIBUTE].startswith(LENS_DETAILS_SUFFIX):
                            lens_url = SITE_URL + '/' + link[HTML_HREF_ATTRIBUTE]

                lens = {'name': unicode(link.text), 'lenstype': unicode(lens_type), 'url': lens_url}

                self.logger.debug(unicode("[{}]: [{}]").format(lens['name'], lens['url']))

                lenses.append(lens)

        return lenses

    @staticmethod
    def convert_to_oakleydb_lens_details(lens, oreview_lens_details):
        if oreview_lens_details is None:
            return None

        lens_details = ObjectFactory.create_lens_details(lens)

        if 'Lens' in oreview_lens_details:
            lens_details['name'] = oreview_lens_details['Lens']
        if 'Base' in oreview_lens_details:
            lens_details['base'] = oreview_lens_details['Base']
        if 'Coating' in oreview_lens_details:
            lens_details['coating'] = oreview_lens_details['Coating']
        if 'Light' in oreview_lens_details:
            lens_details['transmission'] = oreview_lens_details['Light']
        if 'Index' in oreview_lens_details:
            lens_details['transindex'] = oreview_lens_details['Index']
        if 'Purpose' in oreview_lens_details:
            lens_details['purpose'] = oreview_lens_details['Purpose']
        if 'Lighting' in oreview_lens_details:
            lens_details['lighting'] = oreview_lens_details['Lighting']
        if 'Type' in oreview_lens_details:
            lens_details['lenstype'] = oreview_lens_details['Type']

        return lens_details

    @staticmethod
    def convert_to_oakleydb_model_details(model, oreview_model_details):
        if oreview_model_details is None:
            return None

        model_details = ObjectFactory.create_model_details(model)

        if 'Frame' in oreview_model_details:
            model_details['frame'] = oreview_model_details['Frame']
        if 'Lens' in oreview_model_details:
            model_details['lens'] = oreview_model_details['Lens']
        if 'Release Date' in oreview_model_details:
            model_details['releasedate'] = oreview_model_details['Release Date']
        if 'Retire Date' in oreview_model_details:
            model_details['retiredate'] = oreview_model_details['Retire Date']
        if 'Model' in oreview_model_details:
            model_details['style'] = oreview_model_details['Model']
        if 'SKU#' in oreview_model_details:
            model_details['sku2'] = oreview_model_details['SKU#']
        if 'UPC' in oreview_model_details:
            model_details['upc'] = oreview_model_details['UPC']
        if 'USD' in oreview_model_details:
            model_details['usd'] = oreview_model_details['USD']

        return model_details
