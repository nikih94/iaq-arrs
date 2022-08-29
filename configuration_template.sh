#!/bin/bash


####
#
#   INSTRUCTIONS:
#	setup variables and then rename the file to configuration.sh
#
####



####
#
#   GENERAL CONFIG
#
####

#Each sensor must have a different host name
SENSOR_HOSTNAME=my-name
#Each sensors share the same username
USER_ON_RASPI=pi




####
#
#   CONFIG FILE FOR DATA COLLECTION
#
####

#delta in seconds between taken measurments
MEASUREMENT_DELTA=60
#number of raw sensor lines to store in log (43200 = 4weeks) 
SENSOR_LINES=43200 
#Name of the influxdb bucket on the server where IAQ data will be stored
INFLUX_IAQ_BUCKET=iaq
#Server address 
INFLUX_URL=
#Organization name
INFLUX_ORG=
#Token for writing to INFLUX_IAQ_BUCKET and INFLUX_LOG_BUCKET
INFLUX_TOKEN=
#Elapsed time to delete a sent request in milliseconds
INFLUX_TIMEOUT=20000
#Name of the influxdb bucket on the server where logs will be stored
INFLUX_LOG_BUCKET=rpi_stats
#Same as the SENSOR_HOSTNAME
SENSOR_ID=${SENSOR_HOSTNAME}
#Identifier of the building in which the sensor will be placed
BUILDING=my-home
#Local DB setup, no need to change
LOCAL_DB_HOST=host.docker.internal
LOCAL_DB_DATABASE=local-aq
LOCAL_DB_USERNAME=innorenew
LOCAL_DB_PASS=22extrasecret45


####
#
#   CONFIG FILE FOR REVERSE PROXY
#
####

#port on the server that must be configured to allow SSH tcp forwarding
SERVER_PORT=
#ssh port on raspi, default 22
RASPI_PORT=
#user on the server, that will be used to create the SSH tunnel
SENSOR_USER=
#Server ip
SERVER_IP=



####
#
#   CONFIG FILE TELEGRAF
#
####

#Name of the influxdb bucket on the server where sensor stats will be stored
TELEGRAF_BUCKET=rpi_stats
#Token placeholder that will be replaced later by the token
TELEGRAF_TOKEN_PLACEHOLDER='$INFLUX_TOKEN'
#The telegraf token to write data on the TELEGRAF_BUCKET
TELEGRAF_TOKEN=



####
#
#   SSH KEYS
#
####

#No need to change, just point at where SSH_KEYS are located
SSH_PUBLIC=./ssh_keys/id_rsa.pub
SSH_PRIVATE=./ssh_keys/id_rsa