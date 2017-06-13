import time
from core.logger import Logger


class FamilyDal(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def family_exists(self, family_name):
        family = self.get_family(family_name)

        exists = False
        if 'name' in family and family['name'] == family_name:
            exists = True

        return exists

    def get_family(self, family_name):
        family_query = ("SELECT id, name FROM family "
                        "WHERE name = %s "
                        "AND validfrom < %s "
                        "AND ((validto = '0000-00-00 00:00:00') OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        family_data = (family_name, now, now)

        self.logger.debug("Getting family with query [%s] and data [%s]", family_query, family_data)

        cursor.execute(family_query, family_data)

        family = {}
        for (f_id, f_name) in cursor:
            if f_name == family_name:
                family['id'] = f_id
                family['name'] = f_name

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return family

    def get_family_id(self, family_name):
        family_query = ("SELECT id, name FROM family "
                        "WHERE name = %s "
                        "AND validfrom < %s "
                        "AND ((validto = '0000-00-00 00:00:00') OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        family_data = (family_name, now, now)

        self.logger.debug("Getting family id with query [%s] and data [%s]", family_query, family_data)

        cursor.execute(family_query, family_data)

        family_id = -1
        for (f_id, f_name) in cursor:
            if f_name == family_name:
                family_id = f_id

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return family_id

    def get_last_family_id(self):
        family_query = ("SELECT MAX(id) FROM family")

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(family_query)

        ret_id = -1
        for f_id in cursor:
            if f_id is not None and f_id[0] is not None:
                ret_id = int(f_id[0])

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return ret_id

    def insert_family(self, family_name, source_id):
        add_family = ("INSERT INTO family "
                      "(id, name, sourceid, validfrom) "
                      "VALUES (%s, %s, %s, %s)")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        family_id = self.get_last_family_id() + 1

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        data_family = (family_id, family_name, source_id, now)
        cursor.execute(add_family, data_family)

        cnx.commit()

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return family_id
