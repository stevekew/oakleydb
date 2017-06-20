import urllib2
from core import settings
from core.logger import Logger
import json
from core.archivedotcom import ArchiveDotOrg
import os
import errno

URL = 'http://web.archive.org/web/*/http://o-review.com/images//*'

URL2='http://web.archive.org/cdx/search?url=http%3A%2F%2Fo-review.com%2Fimages%2F%2F&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&_=1497711743092'
settings.LOGGING_FILENAME = 'wayback_images'

logger = Logger('data_loader').get()

try:
    response = urllib2.urlopen(URL2)
except urllib2.HTTPError, e:
    logger.info("Failed to open URL [{}]: [{}]".format(URL2, e))
    # return None

html_doc = response.read()

# print html_doc

json_data = json.loads(html_doc)
print len(json_data)
print (json_data[0])

# d = json_data[15000]

# print json_data[1]
wayback = ArchiveDotOrg()
#
# wayback.download_archived_file('http://www.o-review.com:80/glasses.asp', 'test.gif')

cwd = os.getcwd()

count = -1
num = len(json_data)

for d in json_data:
    count += 1

    if count == 0:
        continue

    trimmed_url = d[0].replace("http://", "")
    trimmed_url = trimmed_url.replace("www.", "")
    trimmed_url = trimmed_url.replace("o-review.com", "")
    trimmed_url = trimmed_url.replace(":80", "")
    # print trimmed_url

    split_url = filter(None, trimmed_url.split("/"))
    # print split_url

    dl_path = os.path.join(cwd, *split_url)
    # print dl_path

    if 'Collections' in split_url:
        print 'Not downloading [{}] as it has \'Collections\' in the path'.format(dl_path)
        continue

    if 'Collectors' in split_url:
        print 'Not downloading [{}] as it has \'Collectors\' in the path'.format(dl_path)
        continue

    if 'Forum' in split_url:
        print 'Not downloading [{}] as it has \'Forum\' in the path'.format(dl_path)
        continue

    if 'Gallery' in split_url:
        print 'Not downloading [{}] as it has \'Gallery\' in the path'.format(dl_path)
        continue

    if 'gallery' in split_url:
        print 'Not downloading [{}] as it has \'gallery\' in the path'.format(dl_path)
        continue

    if 'User' in split_url:
        print 'Not downloading [{}] as it has \'User\' in the path'.format(dl_path)
        continue

    if 'user' in split_url:
        print 'Not downloading [{}] as it has \'user\' in the path'.format(dl_path)
        continue

    if not os.path.exists(dl_path):
        print 'Downloding [{}] to [{}]'.format(d[0], dl_path)

        if not os.path.exists(os.path.dirname(dl_path)):
            try:
                print 'Creating directory for [{}]'.format(dl_path)
                os.makedirs(os.path.dirname(dl_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        wayback.download_archived_file(d[0], dl_path)
    else:
        print 'Not downloading [{}] as it already exists on the local drive'.format(dl_path)

    if count % 100 == 0:
        print 'Downloaded [{}] of [{}] files'.format(count, num)



