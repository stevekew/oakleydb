from core.logger import Logger
import time


class MappingDal(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def style_family_mapping_exists(self, style_id, family_id):
        mapping_id = self.get_style_family_mapping_id(style_id, family_id)

        return mapping_id != -1

    def get_style_family_mapping_id(self, style_id, family_id):
        query = ("SELECT id, styleid, familyid FROM familystylemap "
                 "WHERE styleid = %s "
                 "AND familyid = %s "
                 "AND validfrom < %s "
                 "AND ((validto = '0000-00-00 00:00:00') OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        data = (style_id, family_id, now, now)
        self.logger.debug("Getting mapping with query [%s] and data [%s]", query, data)

        cursor.execute(query, data)

        mapping_id = -1
        for (c_id, c_styleid, c_familyid) in cursor:
            if c_styleid == style_id and c_familyid == family_id:
                mapping_id = c_id

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return mapping_id

    def get_last_style_family_mapping_id(self):
        style_query = "SELECT MAX(id) FROM familystylemap"

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(style_query)

        ret_id = -1
        for c_id in cursor:
            if c_id is not None and c_id[0] is not None:
                ret_id = int(c_id[0])

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return ret_id

    def insert_style_family_mapping(self, style_id, family_id, source_id):
        query = ("INSERT INTO familystylemap "
                 "(id, styleid, familyid, sourceid, validfrom) "
                 "VALUES (%s, %s, %s, %s, %s)")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        mapping_id = self.get_last_style_family_mapping_id() + 1

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        data = (mapping_id, style_id, family_id, source_id, now)
        cursor.execute(query, data)

        cnx.commit()

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return mapping_id
