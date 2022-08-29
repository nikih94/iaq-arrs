#!/usr/bin/env python
import serial
import binascii
s = serial.Serial()
s.baudrate = 19200
s.port = '/dev/ttyAMA0'
s.bytesize = serial.EIGHTBITS
s.stopbits = serial.STOPBITS_TWO
s.parity = serial.PARITY_NONE
s.write_timeout = 1
s.open()
# (0x01,0x04,0x00,0x00,0x00,0x24,0xf0,0x11)
command = b'\x01\x04\x00\x00\x00\x24\xf0\x11'
s.write(command)

buf = s.read(100)
print(binascii.hexlify(bytearray(buf)))


print("End of program.")
