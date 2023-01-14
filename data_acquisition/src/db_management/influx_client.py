from configuration import Configuration
from nturl2path import url2pathname
from socket import timeout
import influxdb_client
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import math
from retry import retry
from influxdb_client.client.exceptions import InfluxDBError
from dateutil.parser import parse


class InfluxDB:

    # configuration
    configuration = None
    # the connection
    influxdb_client = None

    test_retry_count = 0

    def __init__(self, configuration):
        self.configuration = configuration
        pass

    """
    Verify connection if exists else create connection
    """

    def connectDB(self):
        if self.influxdb_client == None or not self.influxdb_client.ping():
            self.influxdb_client = InfluxDBClient.from_config_file(
                './configuration.ini')

    def test_retry(self):
        print("Testing retry: ", self.test_retry_count, flush=True)
        if self.test_retry_count < 1:
            self.test_retry_count += 1
            raise

    """
    CONVERT nan to NULL for the mysql to work
    cut also the float precision to some normal decimals
    """

    def clta(self, sensor_data):
        digits = 4  # digits to round float numbers
        l = []
        for i in sensor_data:
            try:
                if math.isnan(float(i)):
                    l.append("NULL")
                else:
                    l.append(round(float(i), digits))
            except ValueError:
                l.append(i)
        return l

    """
    CONVERT nan to NULL for the mysql to work
    cut also the float precision to some normal decimals
    """

    def clean_data(self, sensor_data):
        digits = 4  # digits to round float numbers
        l = []
        for i in range(11):
            if i == 10:  # test if timestamp is string!!
                parse(sensor_data[i], fuzzy=False)
                l.append(sensor_data[i])
            elif i == 6:
                if math.isnan(float(sensor_data[i])):
                    l.append("NULL")
            else:
                l.append(round(float(sensor_data[i]), digits))
        return l

    """
    SEND THE DATA TO THE CENTRAL DB
    """

    def save_to_central_db(self, sensor_data):
        # check connection
        self.connectDB()
        write_api = self.influxdb_client.write_api(
            write_options=SYNCHRONOUS)
        # insert the data
        point = Point("iaq_data").field("temperature", sensor_data[0]).field("RH", sensor_data[1]).field("dew_point", sensor_data[2]).field("abs_humidity", sensor_data[3]).field(
            "co2", sensor_data[4]).field("voc_index", sensor_data[5]).field("voc_acc", sensor_data[6]).field("voc_eq_co2", sensor_data[7]).field("luminance", sensor_data[8]).field("turned_on", sensor_data[9]).time(sensor_data[10])
        write_api.write(bucket=self.configuration.iaq_bucket, record=point)
        write_api.close()
