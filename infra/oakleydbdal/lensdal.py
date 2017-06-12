import time
from core.logger import Logger
from oakleydb.objectfactory import ObjectFactory


class LensDal(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def lens_exists(self, lens_details):
        db_details = self.get_lens_details(lens_details['name'], lens_details['lenstype'])

        exists = False
        if lens_details['name'] == db_details['name'] and lens_details['lenstype'] == db_details['lenstype']:
            exists = True

        return exists

    def get_lens_details(self, lens_name, lens_type):
        query = (
        "SELECT l.id, l.name, base, coating, transmission, transindex, purpose, lighting, url, t.name as lenstype, t.id as typeid FROM lens l "
        "JOIN lenstype t on l.typeid = t.id "
        "WHERE l.name = %s "
        "AND t.name = %s "
        "AND l.validfrom < %s "
        "AND ((l.validto = 0) OR (l.validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        query_data = (lens_name, lens_type, now, now)

        self.logger.debug("Getting lens details with query [%s] and data [%s]", query, query_data)

        cursor.execute(query, query_data)

        lens_details = ObjectFactory.create_lens_details({})

        for (c_lensid, c_lensname, c_base, c_coating, c_transmission, c_transindex, c_purpose, c_lighting, c_url,
             c_lenstype, c_typeid) in cursor:
            if c_lensname == lens_name and c_lenstype == lens_type:
                lens_details['id'] = c_lensid
                lens_details['name'] = c_lensname
                lens_details['base'] = c_base
                lens_details['coating'] = c_coating
                lens_details['transmission'] = c_transmission
                lens_details['transindex'] = c_transindex
                lens_details['purpose'] = c_purpose
                lens_details['lighting'] = c_lighting
                lens_details['url'] = c_url
                lens_details['lenstype'] = c_lenstype
                lens_details['typeid'] = c_typeid

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return lens_details

    def get_last_lens_id(self):
        query = ("SELECT MAX(id) FROM lens")

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(query)

        ret_id = -1
        for f_id in cursor:
            if not f_id[0] is None:
                ret_id = int(f_id[0])

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return ret_id

    def get_last_lens_type_id(self):
        query = ("SELECT MAX(id) FROM lenstype")

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(query)

        ret_id = -1
        for f_id in cursor:
            if not f_id[0] is None:
                ret_id = int(f_id[0])

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return ret_id

    def insert_lens_details(self, lens_details, source_id):

        query = ("INSERT INTO lens "
                 "(id, name, base, coating, transmission, transindex, purpose, lighting, url, typeid, sourceid, validfrom, validto) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        lens_id = self.get_last_lens_id() + 1

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        query_data = (
        lens_id, lens_details['name'], lens_details['base'], lens_details['coating'], lens_details['transmission'],
        lens_details['transindex'], lens_details['purpose'], lens_details['lighting'], lens_details['url'],
        lens_details['typeid'], source_id, now)
        cursor.execute(query, query_data)

        cnx.commit()

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return lens_id

    def lens_type_exists(self, type_name):
        type_id = self.get_lens_type_id(type_name)

        return type_id > -1

    def get_lens_type_id(self, type_name):
        query = ("SELECT id, name FROM lenstype "
                 "WHERE name = %s "
                 "AND validfrom < %s "
                 "AND ((validto = 0) OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        query_data = (type_name, now, now)

        self.logger.debug("Checking if lens type exists with query [%s] and data [%s]", query, query_data)

        cursor.execute(query, query_data)

        type_id = -1
        for (lt_id, lt_name) in cursor:
            if lt_name == type_name:
                type_id = lt_id

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return type_id

    def insert_lens_type(self, type_name, source_id):
        query = ("INSERT INTO lenstype "
                 "(id, name, sourceid, validfrom, validto) "
                 "VALUES (%s, %s, %s, %s, 0)")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        type_id = self.get_last_lens_type_id() + 1

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        query_data = (type_id, type_name, source_id, now)
        cursor.execute(query, query_data)

        cnx.commit()

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return type_id
