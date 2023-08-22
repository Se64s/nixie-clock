#
# app_logger.py
# Brief: Class to generate loggers
#

import logging

APP_LOG_LVL = logging.DEBUG
APP_LOG_FORMAT = "%(name)s : %(message)s"

def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(APP_LOG_LVL)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(APP_LOG_LVL)
    formatter = logging.Formatter(APP_LOG_FORMAT)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log

# EOF
