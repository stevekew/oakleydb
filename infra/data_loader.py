from oakleydbdal.familydal import FamilyDal
from oakleydbdal.styledal import StyleDal
from oakleydbdal.modeldal import ModelDal
from oakleydbdal.connectionpool import ConnectionPool
from core import settings
from loaders import loaderfactory

settings.LOGGING_FILENAME = 'data_loader'


cnx_pool = ConnectionPool(settings.db_config)
dal = ModelDal(cnx_pool)
sd = StyleDal(cnx_pool)
# dal = FamilyDal(cnx_pool)

data_loader = loaderfactory.get_loader(loaderfactory.OREVIEWV1_LOADER)

# families = data_loader.get_family_list()
#
# print families

# styles = data_loader.get_style_list()

# print styles
styles = sd.get_all_styles()

for style in styles:
    models = data_loader.get_models_for_style(style['url'])
    # print models
    for model in models:
        if not dal.model_exists(model['name']):
            print model['name']
            dal.insert_model(model['name'], style['id'], model['sku'], model['listprice'], model['url'], 1)

# ex = dal.family_exists('X-Metal')
# print ex
#
# fid = dal.get_last_family_id()
# print fid
#
# sdal = StyleDal(cnx_pool)
#
# ex = sdal.style_exists('Juliet')
# print ex
#
# style = sdal.get_style('Juliet')
# print style
#
# sid = sdal.get_last_style_id()
# print sid


