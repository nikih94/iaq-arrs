#!/usr/bin/env python
import logging
import sched
import time
import struct
import link_to_sensor
import local_db_manager
import influx_client
import configparser
import log_errors


class CollectData:

    """
    THE LOGGER logas events on file, stdout and central influxdb
    """
    logger = None

    """
    The central DB object
    """
    central_database = None

    """
    Sensor reader
    """
    sensor_reader = None

    """
    Local DB
    """
    local_database = None

    # time interval between taken measuraments in seconds
    delta = 1

    def __init__(self):
        self.load_configuration()
        self.logger.error("data collection restarted")
        pass

    """

    Load the configuration from the config file

    """

    def load_configuration(self):
        config = configparser.ConfigParser()
        config.read('configuration.ini')
        # instantiate influxdb
        self.central_database = influx_client.CentralDB(
            config['data_acquisition'].get('iaq_bucket'), config['influx2'].get('log_bucket'))
        # general conf
        self.delta = config['data_acquisition'].getint('measurement_delta')
        # configure logging
        log_errors.CENTRAL_DB = self.central_database
        self.logger = log_errors.get_logger("error_logger")
        # instantiate sensor reader
        self.sensor_reader = link_to_sensor.Sensor(
            config['data_acquisition'].getint('sensor_lines'), self.logger)
        # # configure local mysql
        self.local_database = local_db_manager.LocalDB(self.logger, config['local_db'].get('local_db_host'), config['local_db'].get(
            'local_db_database'), config['local_db'].get(
            'local_db_username'), config['local_db'].get(
            'local_db_password'))

    """

    Run the Event loop every DELTA seconds

    """

    def main_event_loop(self, sc):
        print("Read data...")
        s.enter(self.delta, 1, self.main_event_loop, (sc,))
        # do your stuff
        try:
            self.sensor_reader.run_sync_client()
            sensor_data = self.sensor_reader.read_sensor()
        except Exception as e:
            self.logger.error(str(e))
            return
        try:
            self.local_database.save_to_local_db(sensor_data)
        except Exception as e:
            self.logger.error(str(e))
        try:
            self.central_database.save_to_central_db(sensor_data)
        except Exception as e:
            self.logger.error(
                "Error during central-INFLUX db insertion: " + str(e))


"""
Start
"""

if __name__ == "__main__":
    CD = CollectData()
    print("Starting script for collecting data")
    s = sched.scheduler(time.time, time.sleep)
    s.enter(CD.delta, 1, CD.main_event_loop, (s,))  # 1 is priority
    s.run()
