#!/usr/bin/env python
from time import sleep
from random import randint
import sched
import time
import configparser
from queue import PriorityQueue, Empty
from configuration import Configuration
from db_management.db_writer import DB_writer
from error_managment import sensor_e_logger, db_e_logger
from sensing.read_sensor import SensorReader
import sys
from db_management.queue_item import CriticalError
from threading import Thread, Lock


class DataCollector():

    # A priority queue
    queue = None
    # The error logger for the sensor
    sensor_e_logger = None
    # The error logger for the DB writer
    db_e_logger = None
    # Object containing all the configuration
    configuration = None

    # sensing thread
    sensing_thread = None
    # writing thread that writes on db
    writing_thread = None

    delta = 10.0

    def __init__(self):
        self.queue = PriorityQueue()
        self.queue.put(CriticalError("restart", 1))
        self.configuration = Configuration('./configuration.ini')
        sensor_e_logger.QUEUE = self.queue
        self.sensor_e_logger = sensor_e_logger.get_logger("error_logger")
        pass

    def spawn_sensing_thread(self):
        self.sensing_thread = SensorReader(
            self.sensor_e_logger, self.configuration, self.queue)
        self.sensing_thread.start()

    def spawn_writing_thread(self):
        self.writing_thread = DB_writer(
            self.configuration, self.queue)
        self.writing_thread.start()

    def start(self):
        self.spawn_sensing_thread()
        self.spawn_writing_thread()
        self.wait_for_threads()

    def wait_for_threads(self):
        while True:
            if not self.sensing_thread.is_alive():
                self.spawn_sensing_thread()
            if not self.writing_thread.is_alive():
                self.shutdown()
            sleep(self.delta)

    def shutdown(self):
        sys.exit()

    """
    ADD function
    If SensorReader dies verify the queue size and if is empty close the program
    
    """


if __name__ == "__main__":
    print("Sensor reader started")
    sr = DataCollector()
    sr.start()
