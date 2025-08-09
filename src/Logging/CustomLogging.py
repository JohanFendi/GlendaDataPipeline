from logging import getLogger, FileHandler, Logger, Formatter, INFO

#Log level should come from the logging module
def get_logger(fmt:str, logger_name:str, log_file_name:str, log_level:int) -> Logger: 
    logger = getLogger(logger_name)
    logger.setLevel(log_level)
    handler = FileHandler(log_file_name)
    handler.setLevel(log_level)
    formatter = Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
