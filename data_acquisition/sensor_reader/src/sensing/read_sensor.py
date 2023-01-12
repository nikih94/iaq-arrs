from threading import Thread
from sensing.link_to_sensor import Sensor
import sched
import time


class SensorReader(Thread):

    # configuration
    config = None

    # sens using this
    sensor = None

    # log errors
    error_logger = None

    # db queue
    db_queue = None

    # time interval between taken measuraments in seconds
    delta = 1.0

    # The scheduler
    s = None

    def __init__(self, error_logger, config, db_queue):
        super(SensorReader, self).__init__()
        self.config = config
        self.error_logger = error_logger
        self.sensor = Sensor(self.config.sensor_lines, self.error_logger)
        self.db_queue = db_queue
        print("Started sensing thread", flush=True)
        pass

    def run(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(self.delta, 1, self.sensing_loop,
                     (self.s,))  # 1 is priority
        self.s.run()

    """

    Run the Event loop every DELTA seconds

    """

    def sensing_loop(self, sc):
        sc.enter(float(self.config.measurement_delta),
                 1, self.sensing_loop, (self.s,))
        #print(self.sensor.dummy_read(), flush=True)
        self.sensor.run_sync_client()
        print(self.sensor.read_sensor(), flush=True)
