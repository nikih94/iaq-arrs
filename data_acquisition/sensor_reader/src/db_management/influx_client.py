from configuration import Configuration
from nturl2path import url2pathname
from socket import timeout
import influxdb_client
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import math


class InfluxDB:

    # configuration
    configuration = None
    # the connection
    influxdb_client = None

    def __init__(self, configuration):
        self.configuration = configuration
        pass

    """
    Verify connection if exists else create connection
    """

    def connectDB(self):
        if self.influxdb_client == None or not self.influxdb_client.ping():
            self.influxdb_client = InfluxDBClient(
                url=self.configuration.url, token=self.configuration.token, org=self.configuration.org, timeout=self.configuration.timeout, verify_ssl=self.configurationverify_ssl)

    """
    SEND THE LOG DATA TO THE CENTRAL DB
    """

    def save_log(self, log):
        # --setup from config file
        self.connectDB()
        write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
        # insert the data
        message = '' + str(log[0]) + ' at filename: ' + str(log[1]) + ' line number: ' + \
            str(log[2]) + ' fun name: ' + str(log[3]) + \
            ' with message: ' + str(log[4])
        point = Point("logs").tag(
            "application", "data-collection").field("exception", message)
        # point = Point("logs").field("levelname", log[0]).field("filename", log[1]).field(
        #    "lineno", log[2]).field("funcName", log[3]).field("message", log[4])
        write_api.write(bucket=self.configuration.log_bucket, record=point)
        write_api.close()
