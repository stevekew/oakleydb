import os
import logging
import settings


class Logger(object):
    def __init__(self, name):
        name = name.replace('.log', '')
        logger = logging.getLogger(name)  # log_namespace can be replaced with your namespace
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            file_name = os.path.join(settings.LOGGING_DIR, '%s.log' % settings.LOGGING_FILENAME)
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s:%(funcName)s]: %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(settings.DEBUG_LEVEL)
            logger.addHandler(handler)
        self._logger = logger

    def get(self):
        return self._logger
