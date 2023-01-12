#!/usr/bin/env python
from threading import Thread
from time import sleep
from random import random
import sched
import time
import configparser
from pqueue import Queue


class SensorReader(Thread):

    q = None

    def __init__(self, q):
        super(SensorReader, self).__init__()
        self.q = q
        print("started producer****************", flush=True)
        pass

    def run(self):
        c = 0
        while True:
            while c < 100000:
                self.q.put(c)
                if c % 10000 == 0:
                    print("producer", c, flush=True)
                sleep(0.1)
                c += 1
            c = 0
            sleep(2)
