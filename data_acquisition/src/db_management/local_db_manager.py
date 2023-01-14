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

    configuration = None

    # Skip some errors since the local DB takes more time to deploy
    skip_first_errors = 0

    def __init__(self, configuration, logger):
        self.configuration = configuration
        self.logger = logger
        self.db_host = self.configuration.local_db_host
        self.db = self.configuration.local_db_database
        self.db_username = self.configuration.local_db_username
        self.db_password = self.configuration.local_db_password
        self.init_local_db()

    """
    CONNECT TO THE DB
    """

    def init_local_db(self):
        try:
            self.local_connection = mysql.connector.connect(
                host='database',  # self.db_host,
                user=self.db_username,
                password=self.db_password,
                database=self.db,
                port=int(3306))
        except:
            pass

    """
    MAINTAIN PERSISTENT CONNECTION ping and try to reconnect
    """

    def get_local_db_cursor(self):
        try:
            self.local_connection.ping(reconnect=True, attempts=3, delay=5)
        except:
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
            try:
                if math.isnan(float(i)):
                    l.append("NULL")
                else:
                    l.append(round(float(i), digits))
            except ValueError:
                l.append(i)
        return l

    """
    SEND THE DATA TO THE LOCAL DB
    """

    def save_to_local_db(self, data_item):
        try:
            cursor = self.get_local_db_cursor()
        except Exception as e:
            if self.skip_first_errors < 4:
                self.skip_first_errors += 1
            else:
                self.logger.error("Error connecting to local DB " + str(e))
            return
        try:
            sensor_data = self.clean_data(data_item.value)
            row = ("NOW()", sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3], sensor_data[4],
                   sensor_data[5], sensor_data[6], sensor_data[7], sensor_data[8], sensor_data[9])
            sql = """INSERT INTO iaq (Timestamp, temperature, RH, dew_point, abs_humidity, co2, voc_index, voc_acc, voc_eq_co2, luminance, turned_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" % row
        except Exception as e:
            self.logger.error("sensor_data length mismatch " + str(e))
            return
        try:
            cursor.execute(sql)
            self.local_connection.commit()
            self.local_connection.close()
        except Exception as e:
            self.logger.error("Error during local db insertion: " +
                              sql + "    except: " + str(e))
            self.local_connection.rollback()
            return
