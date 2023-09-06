import minimalmodbus
import serial
from sensing import decoding_sensor, file_manager
import json
import datetime
import math
import time
import calendar
from datetime import datetime


class Sensor:

    """
    THE LOGGER logas events on file, stdout and central influxdb
    """
    logger = None

    # the file on wich raw data will be logged
    raw_log_file = 'log/raw_log.json'

    # one-million counter
    r_counter = 0

    #
    sensor_lines = 14400

    instrument = None

# write limits, for debug give 1 and 10
    # write to file limit
    w_limit = 1  # 100
    # truncate file limit, every x lines will truncate
    t_limit = 10  # 1000

    def __init__(self, sensor_lines, logger):
        self.logger = logger
        self.sensor_lines = sensor_lines
        pass

    def raw_count(self):
        if self.r_counter > 1000000:
            self.r_counter = 0
        else:
            self.r_counter = self.r_counter + 1

    """
    SYNC WITH THE AQ SENSOR

    debug=True will output more infos

    """

    def run_sync_client(self):
        self.instrument = minimalmodbus.Instrument(port='/dev/serial0', slaveaddress=1, mode=minimalmodbus.MODE_RTU,
                                                   close_port_after_each_call=False, debug=False)  # port name, slave address (in decimal)
        #instrument.precalculate_read_size = False
        self.instrument.serial.baudrate = 19200         # Baud
        self.instrument.serial.bytesize = serial.EIGHTBITS  # !!IMPORTANT!!
        self.instrument.serial.parity = serial.PARITY_NONE  # !!IMPORTANT!!
        self.instrument.serial.stopbits = serial.STOPBITS_ONE  # !!IMPORTANT!!
        self.instrument.serial.timeout = 2.0        # !!IMPORTANT!!
        #instrument.handle_local_echo = True

    """
    Log a raw row of data and maintain the log file

    """

    def log_raw(self, data):
        data = decoding_sensor.decode_all_to_hex(data)
        data_string = ''
        for el in data:
            data_string = data_string + str(el)
        # create the JSON object with datetime
        raw_line = {
            "date": datetime.now().isoformat(),
            "count": str(self.r_counter),
            "raw_data": data_string
        }
        with open(self.raw_log_file, 'a') as outfile:
            line = json.dumps(raw_line, cls=file_manager.DateTimeEncoder)
            line = "\n" + line
            outfile.write(line)
        if self.r_counter % self.t_limit == 0:
            file_manager.truncate_file(
                self.raw_log_file, self.sensor_lines)  # 00)  # ten days

    """
    Read data from the sensor 

    """

    def read_sensor(self):
        try:
            self.run_sync_client()
        except Exception as e:
            self.logger.error("Failed to sync to sensor: "+str(e))
            raise
        try:
            # function from minimalmodbus
            res = self.instrument.read_registers(0, 124, 4)
        except Exception as e:
            self.logger.error("Failed to read sensor: "+str(e))
            raise
        try:
            sensor_data = decoding_sensor.decode_data(res, log=False)
        except Exception as e:
            self.logger.error("Failed to decode registers: "+str(e))
            raise
        sensor_data.append(self.get_timestamp())
        # print(sensor_data)
        self.raw_count()
        if self.r_counter % self.w_limit == 0:
            self.log_raw(res)
        return sensor_data

    """
    Read fake values
    """

    def dummy_read(self):
        if self.r_counter == 0:
            self.logger.error("Failed to read sensor: ")
        self.raw_count()
        values = [23.2, 30.1, 4.1, 3.3, 1000.1,
                  700.1, math.nan, 700.1, 234.4, self.r_counter, self.get_timestamp()]
        return values

    """
    return tiumestamp
    """

    def get_timestamp(self):
        return datetime.utcnow().isoformat() + 'Z'
