#!/bin/bash


. ./configuration.sh

# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi


#enable docker-compose daemon
#sudo systemctl enable docker.service
#sudo systemctl enable containerd.service


### Telegraf token and config and start
#export INFLUX_TOKEN=${TELEGRAF_TOKEN}

#telegraf --config ${TELEGRAF_CONFIG_LINK} </dev/null &>/dev/null &


# GET THE CODE FROM GIT
#git clone https://github.com/nikih94/iaq-arrs


####
#
#   GENERATE CONFIG FILE FOR DATA COLLECTION
#
####

cat > configuration.ini <<EOF
[data_acquisition]
measurement_delta=${MEASUREMENT_DELTA}
sensor_lines=${SENSOR_LINES}
iaq_bucket=${INFLUX_IAQ_BUCKET}


[tags]
sensor_id=${SENSOR_ID}
building=${BUILDING}


[local_db]
local_db_host=${LOCAL_DB_HOST}
local_db_database=${LOCAL_DB_DATABASE}
local_db_username=${LOCAL_DB_USERNAME}
local_db_password=${LOCAL_DB_PASS}


[influx2]
url=${INFLUX_URL}
org=${INFLUX_ORG}
token=${INFLUX_TOKEN}
timeout=${INFLUX_TIMEOUT}
verify_ssl=False
log_bucket=${INFLUX_LOG_BUCKET}
EOF


####
#
#   GENERATE UNIT FILE FOR 
#
####



