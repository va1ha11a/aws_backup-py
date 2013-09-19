from VolSnap import email_reports

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.propagate = False

if __name__ == "__main__":
    try:
        result = email_reports.main()    
    except Exception, exc:
        logger.critical("Exception Occurred:")
        logger.critical(exc)
        #TODO: send some kind of alert Possibly email to alert that the whole process is stuffed
    else:
        logger.info("Report Details: " + str(result))
