from oakleydbdal.familydal import FamilyDal
from oakleydbdal.styledal import StyleDal
from oakleydbdal.modeldal import ModelDal
from oakleydbdal.lensdal import LensDal
from oakleydbdal.connectionpool import ConnectionPool
from core import settings
from core.logger import Logger
from loaders import loaderfactory

settings.LOGGING_FILENAME = 'data_loader'

DATA_SOURCE_O_REVIEW_V1_ARCHIVE = 1

logger = Logger('data_loader').get()

logger.info('Setting up connection pool...')
cnx_pool = ConnectionPool(settings.db_config)

logger.info('Creating data access layer...')
dal = ModelDal(cnx_pool)
sd = StyleDal(cnx_pool)
lens_dal = LensDal(cnx_pool)
# dal = FamilyDal(cnx_pool)

logger.info('Creating data loader with data loader name [{}]'.format(loaderfactory.OREVIEWV1_LOADER))
data_loader = loaderfactory.get_loader(loaderfactory.OREVIEWV1_LOADER)

# families = data_loader.get_family_list()
#
# print families

# styles = data_loader.get_style_list()

# print styles
# logger.info('Retrieving styles...')
# styles = sd.get_all_styles()
# logger.info('Got [{}] styles'.format(len(styles)))


# lenses = data_loader.get_lens_list()

## lens_details = data_loader.get_lens_details({'name': 'VR50-Brown Gradient', 'lenstype': 'Gradient', 'url': 'http://www.o-review.com/lensdetail.asp?ID=2556'})


# first process all lens types
lenses = data_loader.get_lens_list()  # this function will provide basic lens information from the lens list page. use it to get lens types and lens names and urls

# type_name = unicode('')
# for lens in lenses:
#     if type_name != lens['lenstype']:
#         type_name = lens['lenstype']
#         print 'inserting [{}]'.format(type_name)
#         lens_dal.insert_lens_type(type_name, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)



process = True

for lens in lenses:

    # if lens['lenstype'] == 'Gradient':
    #     process = True

    if process:
        if not lens_dal.lens_exists(lens):
            lens_details = data_loader.get_lens_details(lens)

            if not lens_dal.lens_type_exists(lens_details['lenstype']):
                lens_type = lens_details['lenstype']
                print 'Inserting lens type: [{}]'.format(lens_type)
                lens_dal.insert_lens_type(lens_type, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)

            if lens_details['typeid'] == -1:
                lens_details['typeid'] = lens_dal.get_lens_type_id(lens_details['lenstype'])

            # if not lens_dal.lens_exists(lens_details): # already checked above
            lens_dal.insert_lens_details(lens_details, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)



# style = sd.get_style('Dangerous (Asian Fit)')
# process = False
#
# # need to find a better way to process all models as it takes too long
# # perhaps load all modesl from db and then match in code
# for style in styles:
#
#     if style['name'] == 'Eye Jacket':
#         process = True
#
#     if process:
#         models = data_loader.get_models_for_style(style['name'], style['url'])
#
#         for model in models:
#
#             if not dal.model_exists(model['name']):
#                 print model['name']
#
#                 fit_id = 0
#
#                 if 'Asian' in model['name']:
#                     fit_id = 1
#
#                 dal.insert_model(style['id'], model['name'], model['sku'], model['frame'], model['lens'], fit_id,
#                                  model['listprice'], model['url'], 1)
#                 logger.info('Inserted model with name [{}]'.format(model['name']))
#             else:
#                 msg = 'Model with name [{}] already exists in the database, ignoring...'.format(model['name'])
#                 print msg
#                 logger.info(msg)

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
