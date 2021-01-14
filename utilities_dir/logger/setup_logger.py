# encoding: utf-8
import logging


###################
## logging
###################

	
def setup_logger(name, log_file, urllib3="urllib3"):
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logging.getLogger(urllib3).setLevel("CRITICAL")

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    

    return logger

