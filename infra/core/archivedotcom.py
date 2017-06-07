import urllib2
import json

ARCHIVE_BASE_URL = 'http://web.archive.org/web/{}/{}'
ERROR_404 = '404'


def is_valid_archive_url(url, date):
    archive_url = ARCHIVE_BASE_URL.format(date, url)

    try:
        response = urllib2.urlopen(archive_url)
    except urllib2.HTTPError, e:
        return False

    html_doc = response.read()

    if ERROR_404 in html_doc:
        return False

    return True


def find_archive_url(url):
    archive_url = 'http://web.archive.org/cdx/search/cdx?url={}&output=json&limit=500'.format(url)

    response = urllib2.urlopen(archive_url)

    html_doc = response.read()

    # print html_doc
    json_data = json.loads(html_doc)

    # each json obj contains the snapshot date
    for d in reversed(json_data):
        if is_valid_archive_url(url, d[1]):
            return ARCHIVE_BASE_URL.format(d[1], url)

    return None
