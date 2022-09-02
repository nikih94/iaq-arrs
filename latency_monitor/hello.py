#!/usr/bin/env python
import logging
import sched
import time
import struct
import influx_client
import configparser
import log_errors
import re
import uuid
import network_test


class LatencyMonitor:
    # time interval between taken measuraments in seconds
    delta = 10

    """

    Run the Event loop every DELTA seconds

    """

    def main_event_loop(self, sc):
        print("Read data...")
        s.enter(self.delta, 1, self.main_event_loop, (sc,))


"""
Start
"""

if __name__ == "__main__":
    print("Main started")
    LM = LatencyMonitor()
    print("Starting script")
    s = sched.scheduler(time.time, time.sleep)
    s.enter(LM.delta, 1, LM.main_event_loop, (s,))  # 1 is priority
    s.run()
