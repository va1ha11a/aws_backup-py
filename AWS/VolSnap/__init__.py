"""Module to automate snapshots of Volumes on AWS."""

#Set up logger for module
import logging
logger = logging.getLogger(__name__)

logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logger_formatter)

logger.addHandler(logger_handler)