"""Module to automate snapshots of Volumes on AWS."""

#Set up logger for module
import logging
import settings

logger = logging.getLogger(__name__)

logger_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_handler = logging.FileHandler(settings.log_file_name)
logger_handler.setFormatter(logger_formatter)

logger.addHandler(logger_handler)
logger.setLevel(settings.log_level)
logger.propagate = False
