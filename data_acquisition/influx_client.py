from nturl2path import url2pathname
from socket import timeout
import influxdb_client
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import math


class CentralDB:

    iaq_bucket = "default"

    log_bucket = "default"

    influxdb_client = None

    def __init__(self, iaq_bucket, log_bucket):
        self.iaq_bucket = iaq_bucket
        self.log_bucket = log_bucket
        pass

    """
    Verify connection if exists else create connection
    """

    def connectDB(self):
        if self.influxdb_client == None or not self.influxdb_client.ping():
            self.influxdb_client = InfluxDBClient.from_config_file(
                "configuration.ini")

    """
    CONVERT nan to NULL for the mysql to work
    cut also the float precision to some normal decimals
    """

    def clean_data(self, sensor_data):
        digits = 4  # digits to round float numbers
        l = []
        for i in sensor_data:
            if math.isnan(float(i)):
                l.append("NULL")
            else:
                l.append(round(float(i), digits))
        return l

    """
    SEND THE DATA TO THE CENTRAL DB
    """

    def save_to_central_db(self, sensor_data):
        try:
            # check connection
            self.connectDB()
            write_api = self.influxdb_client.write_api(
                write_options=SYNCHRONOUS)
            # insert the data
            sensor_data = self.clean_data(sensor_data)
            point = Point("iaq_data").field("temperature", sensor_data[0]).field("RH", sensor_data[1]).field("dew_point", sensor_data[2]).field("abs_humidity", sensor_data[3]).field(
                "co2", sensor_data[4]).field("voc_index", sensor_data[5]).field("voc_acc", sensor_data[6]).field("voc_eq_co2", sensor_data[7]).field("luminance", sensor_data[8]).field("turned_on", sensor_data[9])
            write_api.write(bucket=self.iaq_bucket, record=point)
            write_api.close()
        except Exception as e:
            raise

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
        write_api.write(bucket=self.log_bucket, record=point)
        write_api.close()
