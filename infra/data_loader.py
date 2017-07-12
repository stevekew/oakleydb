from oakleydbdal.familydal import FamilyDal
from oakleydbdal.styledal import StyleDal
from oakleydbdal.modeldal import ModelDal
from oakleydbdal.lensdal import LensDal
from oakleydbdal.mappingdal import MappingDal
from oakleydbdal.connectionpool import ConnectionPool
from core import settings
from core.logger import Logger
from loaders import loaderfactory
from enum import Enum
import argparse

Mode = Enum('Mode', 'families styles models lenstypes lenses enrichmodels')
DATA_SOURCE_O_REVIEW_V1_ARCHIVE = 2
DATA_SOURCE_OAKLEY_DOT_COM_V1 = 3

parser = argparse.ArgumentParser(description='Oakley DB data loader process')
parser.add_argument('mode', choices=['families', 'styles', 'models', 'lenstypes', 'lenses', 'enrichmodels'],
                    help='The mode to run the loader in')
parser.add_argument('--family', help='The glasses family to load model details for')
parser.add_argument('--reverse', action='store_true', help='Reverse the list being processed')
parser.add_argument('--logfile', help='The name of the log file')

args = parser.parse_args()

loader_mode = Mode[args.mode]
process_family = ''
settings.LOGGING_FILENAME = 'data_loader'
reverse = args.reverse

if args.family is not None:
    process_family = args.family

if args.logfile is not None:
    settings.LOGGING_FILENAME = args.logfile.replace('.log', '')

logger = Logger('data_loader').get()

logger.info('Starting data_loader...')
logger.info('Running with the following args: [{}]'.format(args))
logger.info('===============================')

logger.info('Setting up connection pool...')
cnx_pool = ConnectionPool(settings.db_config)

logger.info('Creating data loader with data loader name [{}]'.format(loaderfactory.OREVIEWV1_LOADER))
data_loader = loaderfactory.get_loader(loaderfactory.OREVIEWV1_LOADER)


process = True

if loader_mode == Mode.lenstypes:
    logger.info('Processing Lens types')
    logger.info('Creating data access layer...')
    lens_dal = LensDal(cnx_pool)

    logger.info('Loading lens list from data loader: [{}]'.format(data_loader.get_name()))
    # this function will provide basic lens information from the lens list page. use it to get lens types and lens names
    #  and urls
    lenses = data_loader.get_lens_list()

    type_name = unicode('')
    for lens in lenses:
        if type_name != lens['lenstype']:
            type_name = lens['lenstype']
            logger.info('inserting [{}]'.format(type_name))
            lens_dal.insert_lens_type(type_name, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)

    logger.info('Done')

elif  loader_mode == Mode.lenses:
    logger.info('Processing Lens details')
    logger.info('Creating data access layer...')
    lens_dal = LensDal(cnx_pool)

    logger.info('Loading lens list from data loader: [{}]'.format(data_loader.get_name()))
    # this function will provide basic lens information from the lens list page. use it to get lens types and lens names
    #  and urls
    lenses = data_loader.get_lens_list()

    for lens in lenses:

        # if lens['lenstype'] == 'Gradient':
        #     process = True

        if process:
            if not lens_dal.lens_exists(lens):
                lens_details = data_loader.get_lens_details(lens)

                if not lens_dal.lens_type_exists(lens_details['lenstype']):
                    lens_type = lens_details['lenstype']
                    logger.info('Inserting lens type: [{}]'.format(lens_type))
                    lens_dal.insert_lens_type(lens_type, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)

                if lens_details['typeid'] == -1:
                    lens_details['typeid'] = lens_dal.get_lens_type_id(lens_details['lenstype'])

                # if not lens_dal.lens_exists(lens_details): # already checked above
                logger.info('Inserting lense details for lens [{}]'.format(lens_details['name']))
                lens_dal.insert_lens_details(lens_details, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)

        ## lens_details = data_loader.get_lens_details({'name': 'VR50-Brown Gradient', 'lenstype': 'Gradient', 'url': 'http://www.o-review.com/lensdetail.asp?ID=2556'})
        logger.info('Done')

elif loader_mode == Mode.families:
    logger.info('Processing Glasses families')

    logger.info('Creating data access layer...')
    family_dal = FamilyDal(cnx_pool)

    logger.info('Loading glasses families from data loader: [{}]'.format(data_loader.get_name()))
    # returns a list of family names
    families = data_loader.get_family_list()

    for family in families:
        if not family_dal.family_exists(family):
            logger.info('Inserting family with name [{}]'.format(family))
            family_dal.insert_family(family, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)

    logger.info('Done')

elif loader_mode == Mode.styles:
    logger.info('Processing Glasses styles')

    logger.info('Creating data access layer...')
    style_dal = StyleDal(cnx_pool)
    family_dal = FamilyDal(cnx_pool)
    mapping_dal = MappingDal(cnx_pool)

    logger.info('Loading glasses styles from data loader: [{}]'.format(data_loader.get_name()))
    # returns a list of styles
    styles = data_loader.get_style_list()

    if reverse:
        styles = reversed(styles)

    for style in styles:
        if style['family'] == 'Signature':
            continue

        logger.info('Processing style [{}]...'.format(style['name']))
        style_id = -1
        if not style_dal.style_exists(style['name']):
            # style doesn't exist in the database
            logger.info('Inserting style: [{}]'.format(style['name']))
            style_id = style_dal.insert_style(style['name'], style['url'], DATA_SOURCE_O_REVIEW_V1_ARCHIVE)
        else:
            logger.info('Ignoring style as it already exists')
            style_id = style_dal.get_style_id(style['name'])

        # confirm if the mapping for this style, family id exists
        family_id = family_dal.get_family_id(style['family'])

        if family_id != -1 and style_id != -1:
            if not mapping_dal.style_family_mapping_exists(style_id, family_id):
                logger.info('Inserting mapping for style [{}]: [{}]->[{}]'.format(style['name'], style_id, family_id))
                mapping_dal.insert_style_family_mapping(style_id, family_id, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)

    logger.info('Done')

elif loader_mode == Mode.models:
    logger.info('Processing Glasses details')

    logger.info('Creating data access layer...')
    model_dal = ModelDal(cnx_pool)
    style_dal = StyleDal(cnx_pool)
    lens_dal = LensDal(cnx_pool)

    styles = {}
    if len(process_family) > 0:
        logger.info('Loading glasses styles from database for family [{}]'.format(process_family))
        styles = style_dal.get_styles_for_family(process_family)
    else:
        logger.info('Loading all glasses styles from database')
        styles = style_dal.get_all_styles()

    logger.info('Loaded [{}] styles for processing'.format(len(styles)))

    if reverse:
        styles = reversed(styles)

    for style in styles:
        logger.info('Processing style [{}]...'.format(style['name']))
        models = data_loader.get_models_for_style(style['name'], style['url'])

        if reverse:
            models = reversed(models)

        for model in models:
            logger.info('Processing model [{}]...'.format(model['name']))
            if not model_dal.model_exists(model):
                model_details = data_loader.get_model_details(model)

                fit = 'Standard'
                lens_id = -1

                if 'Asian' in model_details['name']:
                    fit = 'Asian'

                fit_id = model_dal.get_fit_id(fit)

                lens_id = lens_dal.get_or_create_lens_id(model_details['lens'], 'Eyewear', style['family'],
                                                         DATA_SOURCE_O_REVIEW_V1_ARCHIVE)

                if lens_id == -1:
                    logger.error(
                        'Failed to find lens for model [{}], style [{}], sku [{}]'.format(model_details['name'],
                                                                                          style['name'],
                                                                                          model_details['sku']))
                    continue

                logger.info('Inserting model with name [{}], style [{}], sku [{}]'.format(model_details['name'],
                                                                                          style['name'],
                                                                                          model_details['sku']))

                model_dal.insert_model(model_details, style['id'], lens_id, fit_id, DATA_SOURCE_O_REVIEW_V1_ARCHIVE)
            else:
                logger.info('Model with name [{}] already exists in the database, ignoring...'.format(model['name']))

    logger.info('Done')
elif loader_mode == Mode.enrichmodels:
    logger.info('Enriching Glasses details')

    logger.info('Creating data access layer...')
    model_dal = ModelDal(cnx_pool)
    style_dal = StyleDal(cnx_pool)
    lens_dal = LensDal(cnx_pool)

    # styles = [style_dal.get_style('Bottle Rocket')]
    if len(process_family) > 0:
        logger.info('Loading glasses styles from database for family [{}]'.format(process_family))
        styles = style_dal.get_styles_for_family(process_family)
    else:
        logger.info('Loading all glasses styles from database')
        styles = style_dal.get_all_styles()

    logger.info('Loaded [{}] styles for processing'.format(len(styles)))

    if reverse:
        styles = reversed(styles)

    for style in styles:
        logger.info('Processing style [{}]...'.format(style['name']))
        models = data_loader.get_models_for_style(style['name'], style['url'])

        if reverse:
            models = reversed(models)

        for model in models:
            logger.info('Processing model [{}]...'.format(model['name']))
            if model_dal.model_exists(model):
                model_details = data_loader.get_model_details(model)

                logger.info('Updating model with name [{}], style [{}], sku [{}]'.format(model_details['name'],
                                                                                          style['name'],
                                                                                          model_details['sku']))

                model_dal.update_model(model_details, style['id'], DATA_SOURCE_O_REVIEW_V1_ARCHIVE)
            else:
                logger.info('Model with name [{}] does not exist in the database, ignoring...'.format(model['name']))

    logger.info('Done')
else:
    logger.info('No valid command to process')
    logger.info('Done')


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
