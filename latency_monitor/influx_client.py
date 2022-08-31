from nturl2path import url2pathname
from pprint import pprint
from socket import timeout
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import math

from rx import catch


class CentralDB:

    nl_bucket = "default"

    log_bucket = "default"

    mac = "not-set"

    influxdb_client = None

    def __init__(self, nl_bucket, log_bucket, mac):
        self.nl_bucket = nl_bucket
        self.log_bucket = log_bucket
        self.mac = mac
        self.connectDB()
        pass

    """
    SEND THE DATA TO THE CENTRAL DB
    """

    def save_latency_to_db(self, latency_data):
        try:
            # check connection
            self.connectDB()
            pprint(latency_data)
            # --setup from config file
            write_api = self.influxdb_client.write_api(
                write_options=SYNCHRONOUS)
            # insert the data
            points = []
            for data in latency_data:
                points.append(Point("latency").tag("host_mac", self.mac).tag("remote_mac", data[0]).tag(
                    "remote_name", data[1]).field("latency", int(float(data[2]))))
            write_api.write(bucket=self.nl_bucket, record=points)
            write_api.close()
        except Exception as e:
            raise

    """
    Verify connection if exists else create connection
    """

    def connectDB(self):
        if self.influxdb_client == None or not self.influxdb_client.ping():
            self.influxdb_client = InfluxDBClient.from_config_file(
                "configuration.ini")

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
            "application", "network-latency").field("exception", message)
        # point = Point("logs").field("levelname", log[0]).field("filename", log[1]).field(
        #    "lineno", log[2]).field("funcName", log[3]).field("message", log[4])
        write_api.write(bucket=self.log_bucket, record=point)
        write_api.close()
