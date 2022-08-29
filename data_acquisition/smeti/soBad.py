import struct

sensor_data = '04  48  41  D8  0B  18  7F  C0  00  00  7F  C0  00  00  42  25  FB  46  41  4C  F6  DF  41  2A  8B  B6  7F  C0  00  00  7F  C0  00  00  7F  C0  00  00  44  0E  44  24  7F  C0  00  00  7F  C0  00  00  7F  C0  00  00  43  CA  00  00  7F  C0  00  00  7F  C0  00  00  7F  C0  00  00  43  CA  00  00'
# convert string of hex to list format
sensor_bytes = sensor_data.split('  ')

# exclude first two bytes from list
sensor_bytes = sensor_bytes[2:]

# consider first four bytes for temperature
temperature_bytes = ''.join(sensor_bytes[0:4])

# consider four bytes for relative humadity from byte 12 to 16
rel_humadity_bytes = ''.join(sensor_bytes[12:16])

# consider four bytes for vo2 from byte 36 to 40
co2_bytes = ''.join(sensor_bytes[36:40])

# consider four bytes for voc from byte 68 to 72
voc_bytes = ''.join(sensor_bytes[68:72])


temperature_value = struct.unpack('!f', bytes.fromhex(temperature_bytes))[0]

rel_humadity_value = struct.unpack('!f', bytes.fromhex(rel_humadity_bytes))[0]

co2_value = struct.unpack('!f', bytes.fromhex(co2_bytes))[0]

voc_value = struct.unpack('!f', bytes.fromhex(voc_bytes))[0]

print('Temperature: '+temperature_bytes+' = '+str(temperature_value) + ' °C')
print('Relative Humadity: '+rel_humadity_bytes +
      ' = '+str(rel_humadity_value) + '%')
print('CO2: '+co2_bytes+' = '+str(co2_value) + ' ppm')
print('VOC equivalent CO2: '+voc_bytes+' = '+str(voc_value) + ' ppm')


# Testing

data = [16842, 24619, 32704, 0, 32704, 0, 16914]

print(data[0])
print(hex(data[0]))
d = ''.join(hex(data[0]))
d = d[2:]
e = ''.join(hex(data[1]))
e = e[2:]
f = d + e
print(d)
print(e)
print(f)

ex = struct.unpack('!f', bytes.fromhex(f))[0]

print(str(ex))
