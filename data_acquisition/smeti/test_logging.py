import influxdb_client
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import math

import time

import logging
import sys
from logging.handlers import TimedRotatingFileHandler


from pyrsistent import v
FORMATTER = logging.Formatter(
    "%(asctime)s — %(levelname)s — %(filename)s:%(lineno)s — %(funcName)20s() — %(message)s")
LOG_FILE = "log/errors.log"


# need to set from config file
URL = "default"
ORG = "default"
TOKEN = "default"
TIMEOUT = 6000
VERIFY_SSL = False


"""
Send log to central DB
"""


class DB_log_handler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.setLevel(logging.ERROR)
        self.setFormatter(FORMATTER)

    def emit(self, record):
        log = [record.__dict__['levelname'], record.__dict__['filename'], record.__dict__[
            'lineno'], record.__dict__['funcName'], record.__dict__['message']]
        save_to_central_db(log)


"""
Write the log to stdout
"""


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.ERROR)
    return console_handler


"""
Write the log to files, and it creates a new log file every week. This will store the backoup of the last 4 weeks (rollower 3)
"""


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='W3', backupCount=3)
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


"""
SEND THE LOG DATA TO THE CENTRAL DB
"""


def save_to_central_db(log):
    # --setup from config file
    influx_client = InfluxDBClient.from_config_file("influx_config.ini")
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    # insert the data
    point = Point("logs").field("levelname", log[0]).field("filename", log[1]).field(
        "lineno", log[2]).field("funcName", log[3]).field("message", log[4])
    write_api.write(bucket="iaq", record=point)
    influx_client.close()


"""
Start
"""

if __name__ == "__main__":
    my_logger = get_logger("sexy")
    my_logger.debug("mululul")
    time.sleep(1)
    my_logger.error("mululul")
