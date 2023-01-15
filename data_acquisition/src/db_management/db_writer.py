from threading import Thread
from sensing.link_to_sensor import Sensor
from db_management.influx_error_manager import InfluxErrManager
import sched
import time
from queue import PriorityQueue, Empty
from db_management.queue_item import *
import sys
from time import sleep
from error_managment import db_e_logger
from retry import retry
from db_management.local_db_manager import LocalDB
from urllib3.connection import ConnectTimeoutError, ConnectionError
from influxdb_client.rest import ApiException


"""
This thread reads the queue
    sensor measurements are timestamped before sending them to the queue

behaviour:

1.
if receives a message from the SensorReader with high priority then it tries to send this notification to influxDB, it tries to send the message 2x.
If the message is delivered or not it then tries to empty the queue containing measurements
Then it dies if the queue is empty or if it cannot send data to influx

2.
If it receives a restart message, the application was restarted and it tries to send to influx the information that was restarted

3.
If a data item is received through the queue it is sent to influx and retry infinite times!!
Then it is sent to the local_db try just once!!
Any exception is logged with the logger


(need still to implement this!!)
4.
If sensor errors arrive with low priority then handle them and try to send them to influx


"""


class DB_writer(Thread):

    # configuration
    configuration = None

    # priorityqueue
    queue = None
    # influx client for sending data
    influx = None

    local_db = None

    # logg errors
    logger = None

    # boolean signaling that the thread is working!!
    working = False

    def __init__(self, configuration, queue):
        super(DB_writer, self).__init__()
        self.queue = queue
        self.configuration = configuration
        self.influx = InfluxErrManager(self.configuration)
        db_e_logger.INFLUX = self.influx
        self.logger = db_e_logger.get_logger("db_err_logger")
        self.local_db = LocalDB(self.configuration, self.logger)
        pass

    def run(self):
        print("Started writing thread", flush=True)
        while True:
            try:
                self.process_queue_items()
            except Exception as e:
                self.logger.error("Error while reading the queue: " + str(e))

    def process_queue_items(self):
        while True:
            item = self.queue.get()
#            print(item.value, item.entry_counter, flush=True)
            self.router(item)

    """
    Die with fire
    """

    def shutdown(self):
        sys.exit()

    """
    Route items in the queue
    """

    def router(self, queue_item):
        if isinstance(queue_item, CriticalError):
            if queue_item.value == "sensor":
                self.sensor_error()
            if queue_item.value == "restart":
                self.restart()
        if isinstance(queue_item, DataItem):
            self.save_data_item(queue_item)
        if isinstance(queue_item, SensorReadError):
            self.influx.save_sensor_error(queue_item.value)

    def save_data_item(self, queue_item):
        sensor_data = None
        try:
            sensor_data = self.influx.clean_data(queue_item.value)
        except Exception as e:
            self.logger.error(
                "Error during data validation " + str(e) + " data: " + " ".join(str(x) for x in queue_item.value))
            return
        if sensor_data is not None:
            self.save_to_influx(sensor_data)
        self.local_db.save_to_local_db(queue_item)

    """
    Retry infinite times to send data
    """

    @retry(tries=-1, delay=1, jitter=2, max_delay=30)
    def save_to_influx(self, queue_item):
        try:
            self.influx.save_to_central_db(queue_item)
        except ConnectTimeoutError as e:
            # connection timeout retry again
            # do not log
            raise
        except ApiException as e:
            status = e.status  # status code of the HTTP response
            # check if the status code is 4xx - client error!!
            if status != 404 and status != 408 and status != 429 and (status > 399 and status < 500):
                # log the error and return without retry
                self.logger.error(
                    "Error during central-INFLUX db insertion: " + str(e) + " data: " + " ".join(str(x) for x in queue_item.value))
                return
            else:
                # log the error
                self.logger.error(
                    "Error during central-INFLUX db insertion: " + str(e) + " data: " + " ".join(str(x) for x in queue_item.value))
                raise
        except Exception as e:
            # other unknown errors that are not because of the client
            # log them and raise exception to retry
            self.logger.error(
                "Error during central-INFLUX db insertion: " + str(e) + " data: " + " ".join(str(x) for x in queue_item.value))
            raise

    def sensor_error(self):
        try:
            self.influx.sensor_not_responding()
            self.clean_queue()
        except Exception:
            pass
        self.shutdown()

    def restart(self):
        try:
            self.influx.save_restart()
        except:
            pass

    """
    Empty the queue
    if influx is not working die
    """

    def clean_queue(self):
        print("Cleaning queue")
        try:
            while True:
                item = self.queue.get_nowait()
                if isinstance(item, DataItem):
                    self.influx.send_or_die(item)
        except Empty:
            print("Queue empty ", self.queue.qsize())
            pass
        except Exception:  # if influx is not responding die
            pass
