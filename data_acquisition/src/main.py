#!/usr/bin/env python
from time import sleep
from random import randint
from data_transmitter.data_transmitter import DataTransmitter
from sensor_reader.sensor_reader import SensorReader
import sched
import time
import configparser
from pqueue import Queue


if __name__ == "__main__":
    print("Starting script for collecting data")
    q = Queue(path="/iaq-arrs/persistent-queue/queue",
              tempdir="/iaq-arrs/persistent-queue/tmp")
    tr = DataTransmitter(q)
    rx = SensorReader(q)
    rx.start()
    tr.start()
    # wait for thread to finish
    rx.join()
