import logging
import logging.handlers

logger_name = 'ondra'
logfile_name = 'ondra.log'

def create_logger():
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s - %(message)s')

    fileHandler = logging.handlers.TimedRotatingFileHandler(logfile_name, when='h', interval=1)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    return logger
