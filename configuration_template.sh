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


SENSOR_HOSTNAME=my-name

USER_ON_RASPI=pi




####
#
#   CONFIG FILE FOR DATA COLLECTION
#
####

#delta in seconds between measurments
MEASUREMENT_DELTA=60
#number of raw sensor lines to store in log (43200 = 4weeks) 
SENSOR_LINES=43200 
INFLUX_IAQ_BUCKET=iaq
#Influx setup
INFLUX_URL=
INFLUX_ORG=
INFLUX_TOKEN=
INFLUX_TIMEOUT=20000
INFLUX_LOG_BUCKET=rpi_stats
#sensor identification
SENSOR_ID=${SENSOR_HOSTNAME}
BUILDING=my-home
#local DB setup
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
#IR server ip
SERVER_IP=



####
#
#   CONFIG FILE TELEGRAF
#
####

TELEGRAF_BUCKET=rpi_stats
TELEGRAF_TOKEN_PLACEHOLDER='$INFLUX_TOKEN'
TELEGRAF_TOKEN=



####
#
#   SSH KEYS
#
####


SSH_PUBLIC=./ssh_keys/id_rsa.pub
SSH_PRIVATE=./ssh_keys/id_rsa