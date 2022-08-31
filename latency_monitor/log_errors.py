import influxdb_client
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import math

import time

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

from pyrsistent import v
FORMATTER = logging.Formatter(
    "%(asctime)s — %(levelname)s — %(filename)s:%(lineno)s — %(funcName)20s() — %(message)s")
LOG_FILE = "log/errors.log"


LOG_BUCKET = "default"


CENTRAL_DB = None


"""
Send log to central DB
"""


class DB_log_handler(logging.Handler):
    db = None

    def __init__(self,):
        self.db = CENTRAL_DB
        logging.Handler.__init__(self)
        self.setLevel(logging.ERROR)
        self.setFormatter(FORMATTER)

    def emit(self, record):
        log = [record.__dict__['levelname'], record.__dict__['filename'], record.__dict__[
            'lineno'], record.__dict__['funcName'], record.__dict__['message']]
        self.db.save_log(log)


"""
Write the log to stdout
"""


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.ERROR)
    return console_handler


"""
Write the log to files, log files have a maximum size of 100M and saves 3 backups
"""


def get_file_handler():
    #file_handler = TimedRotatingFileHandler(LOG_FILE, when='W3', backupCount=3)
    # keep log files of total size 400M
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=100*1024*1024, backupCount=3)
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.ERROR)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.addHandler(DB_log_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
