from core.logger import Logger
from core.unicodecsv import *
import os

field_type = {
    0: 'DECIMAL',
    1: 'TINY',
    2: 'SHORT',
    3: 'INT',
    4: 'FLOAT',
    5: 'DOUBLE',
    6: 'NULL',
    7: 'TIMESTAMP',
    8: 'LONGLONG',
    9: 'INT24',
    10: 'DATE',
    11: 'TIME',
    12: 'DATETIME',
    13: 'YEAR',
    14: 'NEWDATE',
    15: 'VARCHAR',
    16: 'BIT',
    246: 'NEWDECIMAL',
    247: 'INTERVAL',
    248: 'SET',
    249: 'TINY_BLOB',
    250: 'MEDIUM_BLOB',
    251: 'LONG_BLOB',
    252: 'BLOB',
    253: 'VAR_STRING',
    254: 'STRING',
    255: 'GEOMETRY'}


class OakleyDbExporter(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def export_database(self, export_path):
        self.logger.info("Exporting whole database to export path [{}]".format(export_path))

        query = "SHOW TABLES"
        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(query)

        tables = []
        for (table) in cursor:
            tables.append(table[0])

        self.logger.info("Exporting [{}] tables".format(len(tables)))
        cursor.close()
        self.connection_pool.release_connection(cnx)

        for table_name in tables:
            self.export_table(table_name, export_path)

    def export_table(self, table_name, export_path):
        self.logger.info("Exporting table [{}] to export path [{}]".format(table_name, export_path))
        query = "SELECT * FROM {}".format(table_name)

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(query)

        file_name = os.path.join(export_path, '{}.csv'.format(table_name))

        self.logger.info("Export filename is [{}]".format(file_name))

        with open(file_name, 'wb') as my_file:
            wr = UnicodeWriter(my_file)
            wr.writerow(cursor.column_names)
            wr.writerow(OakleyDbExporter.get_column_types(cursor.description))

            for item in cursor:
                item_list = list(item)
                for count in range(0, len(item_list)):
                    if item_list[count] is None:
                        item_list[count] = 'NULL'

                wr.writerow(item_list)

        cursor.close()
        self.connection_pool.release_connection(cnx)

        self.logger.info("Completed exporting table [{}]".format(table_name))

    @staticmethod
    def get_column_types(column_desc):
        types = []
        for column in column_desc:
            types.append(field_type[column[1]])

        return types
