import time
from core.logger import Logger


class StyleDal(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def style_exists(self, style_name):
        style = self.get_style(style_name)

        exists = False
        if 'name' in style and style['name'] == style_name:
            exists = True

        return exists

    # TODO, work out how to work with the mappings
    def get_all_styles(self):
        style_query = ("SELECT id, name, url FROM style "
                        "WHERE validfrom < %s "
                        "AND ((validto = '0000-00-00 00:00:00') OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        style_data = (now, now)
        self.logger.debug("Getting style with query [%s] and data [%s]", style_query, style_data)

        cursor.execute(style_query, style_data)

        styles = []
        for (s_id, s_name, s_url) in cursor:
            style = {'id': s_id, 'name': s_name, 'url': s_url}

            styles.append(style)

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return styles

    def get_style(self, style_name):
        style_query = ("SELECT id, name, url FROM style "
                        "WHERE name = %s "
                        "AND validfrom < %s "
                        "AND ((validto = '0000-00-00 00:00:00') OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()



        style_data = (style_name, now, now)
        self.logger.debug("Getting style with query [%s] and data [%s]", style_query, style_data)

        cursor.execute(style_query, style_data)

        style = {}
        for (s_id, s_name, s_url) in cursor:
            if s_name == style_name:
                style['id'] = s_id
                style['name'] = s_name
                style['url'] = s_url

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return style

    def get_style_id(self, style_name):
        style_query = ("SELECT id, name FROM style "
                        "WHERE name = %s "
                        "AND validfrom < %s "
                        "AND ((validto = '0000-00-00 00:00:00') OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        style_data = (style_name, now, now)
        self.logger.debug("Getting style ID with query [%s] and data [%s]", style_query, style_data)

        cursor.execute(style_query, style_data)

        style_id = -1
        for (s_id, s_name) in cursor:
            if s_name == style_name:
                style_id = s_id

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return style_id

    def get_last_style_id(self):
        style_query = ("SELECT MAX(id) FROM style")

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

    def insert_style(self, style_name, url, source_id):
        add_style = ("INSERT INTO style "
                       "(id, name, sourceid, url, validfrom) "
                       "VALUES (%s, %s, %s, %s, %s)")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        style_id = self.get_last_style_id() + 1

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        data_style = (style_id, style_name, source_id, url, now)
        cursor.execute(add_style, data_style)

        cnx.commit()

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return style_id


