"""Abstract transport class which defines CRUDX methods
"""
import sys
import time
import pkg_resources
import logging


class Transport(object):
    LOGGER_NAME = 'openhltest'

    def __init__(self, log_file_name):
        if len(logging.getLogger(Transport.LOGGER_NAME).handlers) == 0:
            handlers = [logging.StreamHandler(sys.stdout)]
            if log_file_name is not None:
                handlers.append(logging.FileHandler(log_file_name, mode='w'))
            formatter = logging.Formatter(fmt='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            formatter.converter = time.gmtime
            for handler in handlers:
                handler.setFormatter(formatter)
                logging.getLogger(Transport.LOGGER_NAME).addHandler(handler)
            logging.getLogger(Transport.LOGGER_NAME).setLevel(logging.INFO)
            logging.getLogger(Transport.LOGGER_NAME).info('using python version %s' % sys.version)
            try:
                version = pkg_resources.get_distribution("openhltest").version
                logging.getLogger(Transport.LOGGER_NAME).info('using openhltest version %s' % version)
            except Exception as e:
                logging.getLogger(Transport.LOGGER_NAME).warn("openhltest not installed using pip, unable to determine version")

    def set_debug_level(self):
        logging.getLogger(Transport.LOGGER_NAME).setLevel(logging.DEBUG)

    def set_warn_level(self):
        logging.getLogger(Transport.LOGGER_NAME).setLevel(logging.WARN)

    def set_info_level(self):
        logging.getLogger(Transport.LOGGER_NAME).setLevel(logging.INFO)

    def info(self, message):
        """Add an INFO level message to the logging handlers
        """
        logging.getLogger(Transport.LOGGER_NAME).info(message)

    def warn(self, message):
        """Add a WARN level message to the logging handlers
        """
        logging.getLogger(Transport.LOGGER_NAME).warn(message)

    def debug(self, message):
        """Add a DEBUG level message to the logging handlers
        """
        logging.getLogger(Transport.LOGGER_NAME).debug(message)

    @property
    def OpenHlTest(self):
        """Override this to return the root node of the model
        """
        raise NotImplemented()

    def _create(self, **kwargs):
        """Override this to create a new resource on the server
        """
        raise NotImplementedError()
    
    def _read(self, **kwargs):
        """Override this to read a resource from the server
        """
        raise NotImplementedError()

    def _update(self, **kwargs):
        """Override this to update a resource on the server
        """
        raise NotImplementedError()
    
    def _delete(self, **kwargs):
        """Override this to delete a resource on the server
        """
        raise NotImplementedError()
    
    def _execute(self, **kwargs):
        """Override this to execute an operation on the server
        """
        raise NotImplementedError()
