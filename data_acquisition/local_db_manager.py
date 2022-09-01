from cmath import nan
import mysql.connector
import math


class LocalDB:

    """
    THE LOGGER logas events on file, stdout and central influxdb
    """
    logger = None

    """
    Write to local DB and to global DB
    """

    db_host = 'host.docker.internal'
    db = 'local-aq'
    db_username = 'innorenew'
    db_password = 'innorenew'

    # the connection
    local_connection = None

    def __init__(self, logger, db_host, db, db_username, db_password):
        self.logger = logger
        self.db_host = db_host
        self.db = db
        self.db_username = db_username
        self.db_password = db_password
        self.init_local_db()
        pass

    """
    CONNECT TO THE DB
    """

    def init_local_db(self):
        self.local_connection = mysql.connector.connect(
            host=self.db_host,
            user=self.db_username,
            password=self.db_password,
            database=self.db,
            port=int(3306))

    """
    MAINTAIN PERSISTENT CONNECTION ping and try to reconnect
    """

    def get_local_db_cursor(self):
        try:
            self.local_connection.ping(reconnect=True, attempts=3, delay=5)
        except mysql.connector.Error as err:
            # reconnect your cursor as you did in __init__ or wherever
            self.logger.error("Reconnecting to local DB " + str(err))
            self.init_local_db()
            raise
        return self.local_connection.cursor()

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
    SEND THE DATA TO THE LOCAL DB
    """

    def save_to_local_db(self, sensor_data):
        try:
            cursor = self.get_local_db_cursor()
        except Exception as e:
            self.logger.error("Error connecting to local DB " + str(e))
            raise
        try:
            sensor_data = self.clean_data(sensor_data)
            row = ("NOW()", sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3], sensor_data[4],
                   sensor_data[5], sensor_data[6], sensor_data[7], sensor_data[8], sensor_data[9])
            sql = """INSERT INTO iaq (Timestamp, temperature, RH, dew_point, abs_humidity, co2, voc_index, voc_acc, voc_eq_co2, luminance, turned_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" % row
        except Exception as e:
            self.logger.error("sensor_data length mismatch " + str(e))
            raise
        try:
            cursor.execute(sql)
            self.local_connection.commit()
            self.local_connection.close()
        except Exception as e:
            self.logger.error("Error during local db insertion: " +
                              sql + "    except: " + str(e))
            self.local_connection.rollback()
            raise
