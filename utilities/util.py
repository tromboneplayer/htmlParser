import logging
from datetime import datetime
from configs.log_config import LOG_FILE, LOG_FORMAT, LOG_LEVEL


logger = None


def log_config():
    global logger
    logging.basicConfig(filename = LOG_FILE, level = LOG_LEVEL, format = LOG_FORMAT, filemode='w')
    logger = logging.getLogger()


def log_util(message, level="INFO"):
    global logger
    
    timestampStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    #timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")

    log_util(timestampStr, level, message)
    
    if logger is None:
        log_config()

    level = level.upper()
        
    #hadle these levels: debug info warning error critical
    if level == 'CRITICAL':
        logger.critical(message)
    elif level == 'DEBUG':
        logger.debug(message)
    elif level == 'WARNING':
        logger.warning(message)
    elif level == 'ERROR':
        logger.error(message)
    else:
        logger.info(message)
    

def fix_unprintable(string_parm: str) -> str:
    '''Replace any unprintable characters as needed.'''
    
    return string_parm.replace(chr(8212), "-") #8212 is an emdash, repace with a regular en dash