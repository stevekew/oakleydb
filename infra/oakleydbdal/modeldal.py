import time
from core.logger import Logger


class ModelDal(object):
    def __init__(self, connection_pool):
        self.logger = Logger(self.__class__.__name__).get()
        self.connection_pool = connection_pool

    def model_exists(self, model_name):
        model = self.get_model(model_name)

        exists = False
        if 'name' in model and model['name'] == model_name:
            exists = True

        return exists

    def get_model(self, model_name):
        model_query = ("SELECT id, name, sku, listprice, url FROM model "
                        "WHERE name = %s "
                        "AND validfrom < %s "
                        "AND ((validto is null) OR (validto >= %s))")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        model_data = (model_name, now, now)

        self.logger.debug("Getting model with query [%s] and data [%s]", model_query, model_data)

        cursor.execute(model_query, model_data)

        model = {}
        for (m_id, m_name, m_sku, m_listprice, m_url) in cursor:
            if m_name == model_name:
                model['id'] = m_id
                model['name'] = m_name
                model['sku'] = m_sku
                model['listprice'] = m_listprice
                model['url'] = m_url

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return model

    def get_last_model_id(self):
        model_query = ("SELECT MAX(id) FROM model")

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute(model_query)

        ret_id = -1
        for f_id in cursor:
            if not f_id[0] is None:
                ret_id = int(f_id[0])

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return ret_id

    def insert_model(self, style_id, model_name, model_sku, model_framecolour, model_lens, fit_id, model_listprice,
                     model_url, source_id):

        add_model = ("INSERT INTO model "
                      "(id, name, styleid, sku, listprice, url, framecolour, lens, fitid, sourceid, validfrom) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

        model_id = self.get_last_model_id() + 1

        cnx = self.connection_pool.get_connection()
        cursor = cnx.cursor()

        data_model = (model_id, model_name, style_id, model_sku, model_listprice, model_url, model_framecolour, model_lens, fit_id, source_id, now)
        cursor.execute(add_model, data_model)

        cnx.commit()

        cursor.close()
        self.connection_pool.release_connection(cnx)

        return model_id
