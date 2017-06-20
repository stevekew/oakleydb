import urllib2
import json
from core.logger import Logger
import urllib

ARCHIVE_BASE_URL = 'http://web.archive.org/web/{}/{}'
ERROR_404 = ' 404'


class ArchiveDotOrg(object):
    def __init__(self):
        self.logger = Logger("archivedotorg").get()

    def is_valid_archive_url(self, url, date):

        archive_url = ARCHIVE_BASE_URL.format(date, url)

        try:
            response = urllib2.urlopen(archive_url)
        except urllib2.HTTPError, e:
            self.logger.info("Failed to open URL [{}]: [{}]".format(archive_url, e))
            return False

        if response.code != 200:
            self.logger.error('Received an error code requesting URL: [{}] code: [{}]'.format(archive_url, response.code))
            return False

        # if we don't get back an html file, it's probably not a 404 page, so just return true
        if response.headers.type != 'text/html':
            return True

        # only search for 404 if the page is html/ text
        html_doc = response.read()

        if ERROR_404 in html_doc:
            self.logger.debug("Archive URL [{}] is not valid as it contains 404:\n[{}]".format(archive_url, html_doc))
            return False

        return True

    def remove_spaces(self, url):
        return url.replace(" ", "%20")

    def find_archive_url(self, url):
        archive_url = 'http://web.archive.org/cdx/search/cdx?url={}&output=json&limit=500'.format(url)

        self.logger.info("Searching for latest archived page for URL [{}]".format(url))

        try:
            response = urllib2.urlopen(self.remove_spaces(archive_url))
        except urllib2.HTTPError, e:
            self.logger.info("Failed to open URL [{}]: [{}]".format(archive_url, e))
            return None

        html_doc = response.read()

        # print html_doc
        json_data = json.loads(html_doc)

        if len(json_data) == 0:
            self.logger.error("Failed to find a cached copy for url [{}]".format(url))

        # each json obj contains the snapshot date
        for d in reversed(json_data):
            if d != json_data[0]:  # first data is the headers
                if self.is_valid_archive_url(url, d[1]):
                    return ARCHIVE_BASE_URL.format(d[1], url)

        return None

    # given a url, find the latest valid version and download to a file
    def download_archived_file(self, url, filename):

        archive_url = self.find_archive_url(url)

        if archive_url is None:
            print 'Unable to find an archived version of [{}]'.format(url)
            self.logger.error('Unable to find an archived version of [{}]'.format(url))
            return

        file_response = urllib.URLopener()

        file_response.retrieve(archive_url, filename)
