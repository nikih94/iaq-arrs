import minimalmodbus
import serial
import decoding_sensor
import file_manager
import json
import datetime


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

    def __init__(self, sensor_lines, logger):
        self.logger = logger
        self.sensor_lines = sensor_lines
        pass

    def raw_count(self):
        if self.r_counter > 1000000:
            self.r_counter = 0
        else:
            self.r_counter = self.r_counter + 1
            return str(self.r_counter)

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
            "date": datetime.datetime.now(),
            "count": self.raw_count(),
            "raw_data": data_string
        }
        with open(self.raw_log_file, 'a') as outfile:
            line = json.dumps(raw_line, cls=file_manager.DateTimeEncoder)
            line = "\n" + line
            outfile.write(line)
        file_manager.truncate_file(
            self.raw_log_file, self.sensor_lines)  # 00)  # ten days

    """
    Log if error during reading

    """

    def log_error(self, data):
        data_string = data
        # create the JSON object with datetime
        raw_line = {
            "date": datetime.datetime.now(),
            "count": str(self.r_counter),
            "raw_data": data_string
        }
        with open(self.raw_log_file, 'a') as outfile:
            line = json.dumps(raw_line, cls=file_manager.DateTimeEncoder)
            line = "\n" + line
            outfile.write(line)
        file_manager.truncate_file(
            self.raw_log_file, self.sensor_lines)  # ten days

    """
    Read data from the sensor 

    """

    def read_sensor(self):
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
        self.log_raw(res)
        return sensor_data
