from threading import Thread
from sensing.link_to_sensor import Sensor
import sched
import time
from db_management.queue_item import DataItem, CriticalError
from retry import retry


"""
This thread dies if is not able to read the sensor     MAX_RETRY = 3 times
it also sends a message to the queue with high priority

"""


class SensorReader(Thread):

    MAX_RETRY = 3

    # configuration
    config = None

    # sens using this
    sensor = None

    # log errors
    error_logger = None

    # priority queue
    queue = None

    # time interval between taken measuraments in seconds
    delta = 1.0

    # The scheduler
    s = None
    # event of the scheduler
    e = None

    # counter
    entry_counter = 0

    testing = None

    def __init__(self, error_logger, config, queue):
        super(SensorReader, self).__init__()
        self.config = config
        self.error_logger = error_logger
        self.sensor = Sensor(self.config.sensor_lines, self.error_logger)
        self.queue = queue
        pass

    def run(self):
        print("Started sensing thread", flush=True)
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(self.delta, 1, self.sensing_loop,
                     (self.s,))  # 1 is priority
        self.s.run()

    def count(self):
        if self.entry_counter > 1000000:
            self.entry_counter = 0
        else:
            self.entry_counter += 1

    """

    Run the Event loop every DELTA seconds

    """

    def sensing_loop(self, s):
        self.e = self.s.enter(float(self.config.measurement_delta),
                              1, self.sensing_loop, (self.s,))
        #print(self.sensor.dummy_read(), flush=True)
        try:
            self.read_sensor()
        except Exception as e:
            if not self.s.empty():
                self.s.cancel(self.e)
            self.queue.put(CriticalError("sensor", 1))
        # self.sensor.run_sync_client()
        #self.queue.put((1, self.sensor.read_sensor()))

    """
    Try to read the sensor several times otherwise reboot
    """

    @retry(tries=3, delay=10)
    def read_sensor(self):
        l = self.sensor.read_sensor()
        d = DataItem(l, self.entry_counter)
        self.queue.put(d)
        self.count()
