#!/bin/bash

. ./configuration.sh


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

#check if the configuration is already updated

if [[ -f "../status/configured.tmp" ]]
then
    echo "System already configured."
    exit 0
fi
echo "Start script enable_iaq_monitoring.sh"



### Set HOSTNAME

echo "127.0.0.1    ${SENSOR_HOSTNAME}" |  sudo tee -a  /etc/hosts

sudo hostnamectl set-hostname ${SENSOR_HOSTNAME}



####
#
#   MOVE CONFIGURATION FILES IN CORRECT DIRECTORIES
#
####

#create the local db volume 
docker volume create mariadb-data

#copy the configuration file
cp ./configuration/configuration.ini ./data_acquisition/configuration.ini

#move telegraf configuration in /etc/telegraf/telegraf.conf
cp ./configuration/telegraf.conf /etc/telegraf/telegraf.conf
#copy the telegraf token into
echo "INFLUX_TOKEN=${TELEGRAF_TOKEN}" > /etc/default/telegraf

#collect data service
cp ./configuration/collect_data.service /etc/systemd/system/collect_data.service


#tunnel service
cp ./configuration/tunnel_to_ir.service /etc/systemd/system/tunnel_to_ir.service


####
#
#   ENABLE SERVICES 
#
####


sudo systemctl enable telegraf.service
sudo systemctl enable collect_data.service
sudo systemctl enable tunnel_to_ir.service





echo "end script enable_iaq_monitoring.sh"