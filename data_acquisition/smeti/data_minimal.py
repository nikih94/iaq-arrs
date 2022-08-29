#!/usr/bin/env python
import logging
import minimalmodbus
import serial
import sched
import time


# time interval between taken measuraments in seconds
DELTA = 3
print("Starting script")
s = sched.scheduler(time.time, time.sleep)


# device address
UNIT = 0x01


def run_sync_client():
    instrument = minimalmodbus.Instrument(port='/dev/ttyAMA0', slaveaddress=1, mode=minimalmodbus.MODE_RTU,
                                          close_port_after_each_call=False, debug=True)  # port name, slave address (in decimal)
    instrument.precalculate_read_size = False
    instrument.serial.baudrate = 19200         # Baud
    instrument.serial.bytesize = serial.EIGHTBITS
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = serial.STOPBITS_ONE
    instrument.serial.timeout = 2.0        # seconds
    #instrument.handle_local_echo = True
    #res = instrument.read_registers(0, 36, 4)
    try:
        res = instrument.read_registers(0, 36, 4)
        print(res)
    except IOError:
        print("Failed to read", IOError)


def do_something(sc):
    print("Read data...")
    # do your stuff
    run_sync_client()
    s.enter(DELTA, 1, do_something, (sc,))


if __name__ == "__main__":
    s.enter(DELTA, 1, do_something, (s,))
    s.run()
