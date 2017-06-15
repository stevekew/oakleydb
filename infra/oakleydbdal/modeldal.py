import time
from core.logger import Logger


class ModelDal(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def model_exists(self, model):
        ret_model = self.get_model(model['style'], model['name'], model['sku'])

        exists = False
        if ret_model is not None and 'name' in ret_model and model['name'] == ret_model['name']:
            exists = True

        return exists

    def get_model(self, style_name, model_name, sku):
        query = ("SELECT m.id, m.name, m.sku, m.listprice, m.url FROM model m JOIN style s on m.styleid = s.id "
                        "WHERE s.name = %s "
                        "AND m.name = %s "
                        "AND m.sku = %s "
                        "AND m.validfrom < %s "
                        "AND ((m.validto = 0) OR (m.validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        data = (style_name, model_name, sku, now, now)

        self.logger.debug("Getting model with query [%s] and data [%s]", query, data)

        cursor.execute(query, data)

        model = None
        for (m_id, m_name, m_sku, m_listprice, m_url) in cursor:
            if m_name == model_name and sku == m_sku:
                model = {'id': m_id, 'name': m_name, 'sku': m_sku, 'listprice': m_listprice, 'url': m_url}

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return model

    def get_model_id(self, style_id, model_name, sku):
        query = ("SELECT id, name, sku FROM model "
                        "WHERE name = %s "
                        "AND styleid = %s "
                        "AND sku = %s "
                        "AND validfrom < %s "
                        "AND ((validto = 0) OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        data = ( model_name, style_id, sku, now, now)

        self.logger.debug("Getting model id with query [%s] and data [%s]", query, data)

        cursor.execute(query, data)

        model_id = -1
        for (m_id, m_name, m_sku) in cursor:
            if m_name == model_name and sku == m_sku:
                model_id = m_id

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return model_id

    def get_last_model_id(self):
        model_query = ("SELECT MAX(id) FROM model")

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(model_query)

        ret_id = -1
        for c_id in cursor:
            if c_id is not None and c_id[0] is not None:
                ret_id = int(c_id[0])

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return ret_id

    #style_id, model_name, model_sku, model_framecolour, model_lens, fit_id, model_listprice, model_url
    def insert_model(self,  model, style_id, lens_id, fit_id, source_id):

        query = ("INSERT INTO model "
                      "(name, styleid, sku, listprice, url, framecolour, lensid, fitid, sourceid, validfrom) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        data = (model['name'], style_id, model['sku'], model['listprice'], model['url'],
                      model['frame'], lens_id, fit_id, source_id, now)

        self.logger.debug("Inserting model with query [%s] and data [%s]", query, data)

        cursor.execute(query, data)

        cnx.commit()

        cursor.close()
        self.connection_pool.release_connection(cnx)

        model_id = self.get_model_id(style_id, model['name'], model['sku'])
        return model_id
