from db_management.influx_client import InfluxDB
from retry import retry
from configuration import Configuration
from nturl2path import url2pathname
from socket import timeout
import influxdb_client
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import math


class InfluxErrManager(InfluxDB):

    def __init__(self, configuration):
        super(InfluxErrManager, self).__init__(configuration)

    """
    Send the data or kill the application
    """
    @retry(tries=3, delay=10)
    def send_or_die(self, data_item):
        # check connection
        self.connectDB()
        write_api = self.influxdb_client.write_api(
            write_options=SYNCHRONOUS)
        # insert the data
        sensor_data = self.clean_data(data_item.value)
        point = Point("iaq_data").field("temperature", sensor_data[0]).field("RH", sensor_data[1]).field("dew_point", sensor_data[2]).field("abs_humidity", sensor_data[3]).field(
            "co2", sensor_data[4]).field("voc_index", sensor_data[5]).field("voc_acc", sensor_data[6]).field("voc_eq_co2", sensor_data[7]).field("luminance", sensor_data[8]).field("turned_on", sensor_data[9]).time(sensor_data[10])
        write_api.write(bucket=self.configuration.iaq_bucket, record=point)
        write_api.close()

    """
    Save errors to db
    """

    def save_sensor_error(self, log):
        try:
            # --setup from config file
            self.connectDB()
            write_api = self.influxdb_client.write_api(
                write_options=SYNCHRONOUS)
            # insert the data
            point = Point("logs").tag(
                "application", "data-collection").field("sensor_error", log)
            write_api.write(bucket=self.configuration.log_bucket, record=point)
            write_api.close()
        except Exception:
            pass

    """
    sensor not responding error
    """
    @retry(tries=3, delay=10)
    def sensor_not_responding(self):
        # --setup from config file
        self.connectDB()
        write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
        # insert the data
        point = Point("logs").tag(
            "application", "data-collection").field("sensor_not_responding", 1)
        write_api.write(bucket=self.configuration.log_bucket, record=point)
        write_api.close()

    """
    count restarts
    """
    @retry(tries=3, delay=5)
    def save_restart(self):
        # --setup from config file
        self.connectDB()
        write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
        point = Point("logs").tag(
            "application", "data-collection").field("restart", 1)
        write_api.write(bucket=self.configuration.log_bucket, record=point)
        write_api.close()

    """
    Save errors to db
    """

    def save_db_error(self, log):
        try:
            # --setup from config file
            self.connectDB()
            write_api = self.influxdb_client.write_api(
                write_options=SYNCHRONOUS)
            # insert the data
            point = Point("logs").tag(
                "application", "data-collection").field("db_error", log)
            write_api.write(bucket=self.configuration.log_bucket, record=point)
            write_api.close()
        except Exception:
            pass
