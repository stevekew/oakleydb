from core.logger import Logger
from core.unicodecsv import *
import os


class OakleyForumDbExporter(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def export_database(self, export_path):
        export_name = 'sunglasses'

        self.logger.info("Exporting whole database to export path [{}]".format(export_path))

        query = "select f.name as family, s.name as model,m.name as colorway, m.framecolour as frame, l.name as lens, m.listprice," \
                " m.sku, m.releasedate, m.retiredate, m.note, m.exclusive, m.signature from model m join lens l on" \
                " m.lensid = l.id join style s on m.styleid=s.id join familystylemap x on x.styleid = s.id join" \
                " family f on x.familyid = f.id"

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(query)

        file_name = os.path.join(export_path, '{}.csv'.format(export_name))

        self.logger.info("Export filename is [{}]".format(file_name))

        headers = 'Type,Family,Model,Colorway,Frame,Lens,List Price,SKU,Release Date,Retire Date,Note:,Exclusive,Signature'.split(',')

        with open(file_name, 'wb') as my_file:
            wr = UnicodeWriter(my_file)
            # header
            wr.writerow(headers)

            for item in cursor:
                item_list = list(item)
                item_list.insert(0, 'Sunglasses')
                for count in range(0, len(item_list)):
                    if item_list[count] is None:
                        item_list[count] = ''

                wr.writerow(item_list)

        cursor.close()
        self.connection_pool.release_connection(cnx)

        self.logger.info("Completed exporting table [{}]".format(export_name))
