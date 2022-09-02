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

    """
    THE LOGGER logas events on file, stdout and central influxdb
    """
    logger = None

    """
    The central DB object
    """
    central_database = None

    """
    The network tester
    """
    nt = None

    # time interval between taken measuraments in seconds
    delta = 1

    def __init__(self):
        self.load_configuration()
        self.logger.error("network latency restarted")
        pass

    """

    Load the configuration from the config file

    """

    def load_configuration(self):
        config = configparser.ConfigParser()
        config.read('configuration.ini')
        # # configure influx
        self.central_database = influx_client.CentralDB(config['network_latency'].get('latency_bucket'), config['influx2'].get('log_bucket'), ''.join(re.findall(
            '..', '%012x' % uuid.getnode())))  # retrieve mac address
        # general conf
        self.delta = config['network_latency'].getint('measurement_delta')
        # # configure logging
        log_errors.CENTRAL_DB = self.central_database
        self.logger = log_errors.get_logger("error_logger")
        # configure network test
        self.nt = network_test.NetworkTest(
            config['network_latency'].get('central_server_ip'), config['network_latency'].getint('latency_test_timeout'), self.logger)
        print("Configured")

    """

    Run the Event loop every DELTA seconds

    """

    def main_event_loop(self, sc):
        #print("Read data...")
        s.enter(self.delta, 1, self.main_event_loop, (sc,))
        # do your stuff
        try:
            #print('Load devices')
            self.nt.load_devices()
        except Exception as e:
            self.logger.error(str(e))
            return
        try:
            # print('Measure')
            latency_data = self.nt.measure_latency()
        except Exception as e:
            self.logger.error(str(e))
            return
        try:
            if latency_data != None:
                # print('store')
                self.central_database.save_latency_to_db(latency_data)
        except Exception as e:
            self.logger.error(
                "Error during central-INFLUX db insertion: " + str(e))


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
