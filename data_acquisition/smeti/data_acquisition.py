#!/usr/bin/env python
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import logging
import pymodbus
import serial
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.diag_message import *
from pymodbus.file_message import *
from pymodbus.other_message import *
from pymodbus.mei_message import *
import sched
import time
from pymodbus.constants import Defaults
Defaults.RetryOnEmpty = True


# time interval between taken measuraments in seconds
DELTA = 5
print("Starting script")
s = sched.scheduler(time.time, time.sleep)


FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# device address
UNIT = 0x01


def run_sync_client():
    client = ModbusClient(method='rtu', port='/dev/ttyAMA0',
                          baudrate=19200, timeout=2, parity='N', bytesize=8, stopbits=1)
    client.strict = False  # maybe problem
    #client.stopbits = 2
    print("Conecction succes: ", client.connect())
    print(client.is_socket_open())
    time.sleep(1)
    rr = client.read_input_registers(address=0x00, count=32, unit=UNIT)
    # assert(not rr.isError())     # test that we are not an error
    #print("111", rr.message)
    print("111", rr.registers)
    #print("111", rr.bits)
    print("111", rr)
    for reg in rr.registers:
        hex_string = '0x{:02x}'.format(reg)
        print(hex_string)
    # ----------------------------------------------------------------------- #
    # close the client
    # ----------------------------------------------------------------------- #
    client.close()


def do_something(sc):
    print("Read data...")
    # do your stuff
    run_sync_client()
    s.enter(DELTA, 1, do_something, (sc,))


if __name__ == "__main__":
    s.enter(1, 1, do_something, (s,))
    s.run()


# log.debug("Running ReportSlaveIdRequest")
#     rq = ReportSlaveIdRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     # assert(not rr.isError()) # test that we are not an error
#     # assert(rr.identifier == 0x00) # test the slave identifier
#     # assert(rr.status == 0x00) # test that the status is ok
#     log.debug("Running ReadExceptionStatusRequest")
#     rq = ReadExceptionStatusRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     # assert(not rr.isError()) # test that we are not an error
#     # assert(rr.status == 0x55) # test the status code
#     log.debug("Running GetCommEventCounterRequest")
#     rq = GetCommEventCounterRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     # assert(not rr.isError()) # test that we are not an error
#     # assert(rr.status == True) # test the status code
#     # assert(rr.count == 0x00) # test the status code
#     log.debug("Running GetCommEventLogRequest")
#     rq = GetCommEventLogRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     # assert(not rr.isError()) # test that we are not an error
#     # assert(rr.status == True) # test the status code
#     # assert(rr.event_count == 0x00) # test the number of events
#     # assert(rr.message_count == 0x00) # test the number of messages
#     # assert(len(rr.events) == 0x00) # test the number of events
#     # ------------------------------------------------------------------------#
#     # diagnostic requests
#     # ------------------------------------------------------------------------#
#     log.debug("Running ReturnQueryDataRequest")
#     rq = ReturnQueryDataRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     # assert(rr.message[0] == 0x0000) # test the resulting message
#     log.debug("Running RestartCommunicationsOptionRequest")
#     rq = RestartCommunicationsOptionRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     # assert(rr.message == 0x0000) # test the resulting message
#     log.debug("Running ReturnDiagnosticRegisterRequest")
#     rq = ReturnDiagnosticRegisterRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ChangeAsciiInputDelimiterRequest")
#     rq = ChangeAsciiInputDelimiterRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ForceListenOnlyModeRequest")
#     rq = ForceListenOnlyModeRequest(unit=UNIT)
#     rr = client.execute(rq)  # does not send a response
#     log.debug(rr)
#     log.debug("Running ClearCountersRequest")
#     rq = ClearCountersRequest()
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ReturnBusCommunicationErrorCountRequest")
#     rq = ReturnBusCommunicationErrorCountRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ReturnBusExceptionErrorCountRequest")
#     rq = ReturnBusExceptionErrorCountRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ReturnSlaveNoResponseCountRequest")
#     rq = ReturnSlaveNoResponseCountRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ReturnSlaveNAKCountRequest")
#     rq = ReturnSlaveNAKCountRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ReturnSlaveBusyCountRequest")
#     rq = ReturnSlaveBusyCountRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     log.debug("Running ReturnSlaveBusCharacterOverrunCountRequest")
#     rq = ReturnSlaveBusCharacterOverrunCountRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ReturnIopOverrunCountRequest")
#     rq = ReturnIopOverrunCountRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     # assert(rr == None) # not supported by reference
#     log.debug("Running ClearOverrunCountRequest")
#     rq = ClearOverrunCountRequest(unit=UNIT)
#     rr = client.execute(rq)
#     log.debug(rr)
#     log.debug("Read input registers")
