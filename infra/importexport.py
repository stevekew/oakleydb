from core import settings
from core.logger import Logger
from importexport.oakleydbexporter import OakleyDbExporter
from importexport.oakleydbimporter import OakleyDbImporter
from importexport.oakleyforumexporter import OakleyForumDbExporter
from oakleydbdal.connectionpool import ConnectionPool

settings.LOGGING_FILENAME = 'importexport'

logger = Logger('importexport').get()

logger.info('Starting data_loader...')
# logger.info('Running with the following args: [{}]'.format(args))
logger.info('===============================')

logger.info('Setting up connection pool...')
# settings.db_config['database'] = 'aquariaz_oakleydbtest'

cnx_pool = ConnectionPool(settings.db_config)


# exporter = OakleyDbExporter(cnx_pool)
# importer = OakleyDbImporter(cnx_pool)
oakleyforum = OakleyForumDbExporter(cnx_pool)
oakleyforum.export_database('./')
# exporter.export_database('./csv/')
# importer.import_table('source', './csv/source.csv')
# importer.import_table('family', './csv/family.csv')
