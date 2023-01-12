#!/usr/bin/env python
from time import sleep
from random import randint
import sched
import time
import configparser
from queue import Queue
from configuration import Configuration
from db_management.influx_client import InfluxDB
from error_managment import sensor_e_logger, db_e_logger
from sensing.read_sensor import SensorReader
from threading import Thread


class DataCollector():

    # The queue for sending data to the local DB
    db_queue = None
    # The queue for sending errors
    err_queue = None
    # The error logger for the sensor
    sensor_e_logger = None
    # The error logger for the DB writer
    db_e_logger = None
    # Object containing all the configuration
    configuration = None

    # sensing thread
    sensing_thread = None

    def __init__(self):
        self.db_queue = Queue()
        self.err_queue = Queue()
        self.configuration = Configuration('../configuration.ini')
        self.sensor_e_logger = sensor_e_logger.DB_log_handler(self.err_queue)
        self.db_e_logger = db_e_logger.DB_log_handler(self.err_queue)
        InfluxDB(self.configuration)
        pass

    def spawn_sensing_thread(self):
        self.sensing_thread = SensorReader(
            self.sensor_e_logger, self.configuration, self.db_queue)
        self.sensing_thread.start()
        self.sensing_thread.join()


if __name__ == "__main__":
    print("Sensor reader started")
    sr = DataCollector()
    sr.spawn_sensing_thread()
