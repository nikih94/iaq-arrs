#!/bin/bash


. ./configuration.sh


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi


####
#
#   MOVE CONFIGURATION FILES IN CORRECT DIRECTORIES
#
####


# GET THE CODE FROM GIT
#git clone https://github.com/nikih94/iaq-arrs


#move telegraf configuration in /etc/telegraf/telegraf.conf

#copy the telegraf token into
echo "INFLUX_TOKEN=iOC-xleVA5cThnnsuquj6cB4etopUCa5e4farWi8AFLn5fzzaZDynjPYcB5-ICh4ZWpNwchcWUMKeLRunzk4Ug==" > /etc/default/telegraf



####
#
#   ENABLE SERVICES
#
####




#enable docker-compose daemon
#sudo systemctl enable docker.service
#sudo systemctl enable containerd.service

