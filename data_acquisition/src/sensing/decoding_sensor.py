# Module file: decoding_sensors.py
import struct


# set register address of measuraments
temperature = 0
r_humidity = 6
dew_point = 8
abs_humidity = 10
co2 = 18
voc_index = 26
voc_acc = 28
voc_eq_co2 = 34
luminance = 42
pm10 = 60
pm4 = 62
pm2_5 = 64
pm1 = 66
pressure = 76
turned_on = 84
thermostat = 100


"""
function that decodes the data from binary into IEEE 754
"""


def decode_measurament(data, measurament, log):
    hex_data1 = ''.join(hex(data[measurament]))
    hex_data1 = hex_data1[2:]
    if len(hex_data1) < 4:
        for x in range(0, 4-len(hex_data1)):
            hex_data1 = '0' + hex_data1
    hex_data2 = ''.join(hex(data[measurament+1]))
    hex_data2 = hex_data2[2:]
    if len(hex_data2) < 4:
        for x in range(0, 4-len(hex_data2)):
            hex_data2 = '0' + hex_data2
    hex_data1 = hex_data1 + hex_data2
    if log:
        print("reg: ", measurament, " ", hex_data1)
    return struct.unpack('!f', bytes.fromhex(hex_data1))[0]


"""
main function that will decode the data
allows to select only usefull registers 
returnd a list with decoded data

"""


def decode_data(data, log=False):
    list = []
    list.append(decode_measurament(data, temperature, log))
    list.append(decode_measurament(data, r_humidity, log))
    list.append(decode_measurament(data, dew_point, log))
    list.append(decode_measurament(data, abs_humidity, log))
    list.append(decode_measurament(data, co2, log))
    list.append(decode_measurament(data, voc_index, log))
    list.append(decode_measurament(data, voc_acc, log))
    list.append(decode_measurament(data, voc_eq_co2, log))
    list.append(decode_measurament(data, luminance, log))
    # list.append(decode_measurament(data, pm10, log))  # the sensor is not detecting this features
    #list.append(decode_measurament(data, pm4, log))
    #list.append(decode_measurament(data, pm2_5, log))
    #list.append(decode_measurament(data, pm1, log))
    #list.append(decode_measurament(data, pressure, log))
    list.append(decode_measurament(data, turned_on, log))
    #list.append(decode_measurament(data, thermostat, log))
    return list


"""
other stupid functions

"""


def print_data(list):
    for el in list:
        print(str(el))


def print_data_with_id(list):
    i = 0
    for el in list:
        print("reg: ", i, " ", str(el))
        i = i+2


def decode_all(data):
    list = []
    for i in range(0, len(data), 2):
        list.append(decode_measurament(data, i, log=False))
    return list


def decode_to_hex(data, measurament):
    hex_data1 = ''.join(hex(data[measurament]))
    hex_data1 = hex_data1[2:]
    if len(hex_data1) < 4:
        for x in range(0, 4-len(hex_data1)):
            hex_data1 = '0' + hex_data1
    hex_data2 = ''.join(hex(data[measurament+1]))
    hex_data2 = hex_data2[2:]
    if len(hex_data2) < 4:
        for x in range(0, 4-len(hex_data2)):
            hex_data2 = '0' + hex_data2
    hex_data1 = hex_data1 + hex_data2
    return hex_data1


def decode_all_to_hex(data):
    list = []
    for i in range(0, len(data), 2):
        list.append(decode_to_hex(data, i))
    return list
