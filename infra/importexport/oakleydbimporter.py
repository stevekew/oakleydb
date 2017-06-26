from core.logger import Logger
from core.unicodecsv import *
import os


class OakleyDbImporter(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def import_table(self, table_name, import_file):

        self.logger.info('importing table [{}] from file [{}]'.format(table_name, import_file))
        with open(import_file, 'r') as my_file:
            rr = UnicodeReader(my_file)

            query = "INSERT INTO {} (".format(table_name)

            cnx = self.connection_pool.get_connection()

            # first line is header, column names
            # second line is header, column types
            processed_header = False
            processed_types = False

            field_types = []
            for line in rr:
                if not processed_header:
                    processed_header = True
                    query += ','.join(line)
                    query += ') VALUES ('

                    data_str = '%s,' * len(line)

                    query += data_str.rstrip(',')
                    query += ')'
                elif processed_header and not processed_types:
                    processed_types = True
                    field_types = line
                else:
                    cursor = cnx.cursor()

                    for count in range(0, len(line)):
                        if field_types[count] == 'INT' or field_types[count] == 'BIT':
                            line[count] = int(line[count])
                        elif field_types[count] == 'TIMESTAMP' and line[count] == '0':
                            line[count] = 0

                    self.logger.debug("Updating model with query [%s] and data [%s]", query, line)

                    cursor.execute(query, line)

                    cnx.commit()

                    cursor.close()

            self.connection_pool.release_connection(cnx)

            print 'Done'
            # read out the headers
            # build the qurey
            # import
