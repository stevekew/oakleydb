from oakleydbdal.familydal import FamilyDal
from oakleydbdal.styledal import StyleDal
from oakleydbdal.modeldal import ModelDal
from oakleydbdal.connectionpool import ConnectionPool
from core import settings
from core.logger import Logger
from loaders import loaderfactory

settings.LOGGING_FILENAME = 'data_loader'

logger = Logger('data_loader').get()

logger.info('Setting up connection pool...')
cnx_pool = ConnectionPool(settings.db_config)

logger.info('Creating data access layer...')
dal = ModelDal(cnx_pool)
sd = StyleDal(cnx_pool)
# dal = FamilyDal(cnx_pool)

logger.info('Creating data loader with data loader name [{}]'.format(loaderfactory.OREVIEWV1_LOADER))
data_loader = loaderfactory.get_loader(loaderfactory.OREVIEWV1_LOADER)

# families = data_loader.get_family_list()
#
# print families

# styles = data_loader.get_style_list()

# print styles
logger.info('Retrieving styles...')
styles = sd.get_all_styles()
logger.info('Got [{}] styles'.format(len(styles)))

# style = sd.get_style('Dangerous (Asian Fit)')
process = False

# need to find a better way to process all models as it takes too long
# perhaps load all modesl from db and then match in code

for style in styles:

    if style['family'] == 'Arrays':
        process = True

    if process:
        models = data_loader.get_models_for_style(style['name'], style['url'])

        for model in models:

            if not dal.model_exists(model['name']):
                print model['name']
                dal.insert_model(model['name'], style['id'], model['sku'], model['listprice'], model['url'], 1)
                logger.info('Inserted model with name [{}]'.format(model['name']))
            else:
                msg = 'Model with name [{}] already exists in the database, ignoring...'.format(model['name'])
                print msg
                logger.info(msg)

#             print model['name']
#             dal.insert_model(model['name'], style['id'], model['sku'], model['listprice'], model['url'], 1)
#             logger.info('Inserted model with name [{}]'.format(model['name']))
#         else:
#             msg = 'Model with name [{}] already exists in the database, ignoring...'.format(model['name'])
#             print msg
#             logger.info(msg)

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
