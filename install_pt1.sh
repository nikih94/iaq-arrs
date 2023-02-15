#!/bin/bash

#Load the configuration variables
. ./configuration.sh


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi


#update system
sudo apt-get -y update
sudo apt-get -y upgrade

#then setup UART on raspi4
sudo raspi-config nonint do_serial 1
sudo cp /boot/my_config.txt /boot/config.txt



#set correct timezone
timedatectl set-timezone Europe/Rome

cd /home/${USER_ON_RASPI}/

#Set ssh keys
mkdir -p .ssh && sudo cat ${SSH_PUBLIC} > .ssh/id_rsa.pub && sudo cat ${SSH_PRIVATE} > .ssh/id_rsa && cd .ssh/ && touch known_hosts && sudo chmod 400 id_rsa && sudo chmod 400 id_rsa.pub && sudo chmod 600 known_hosts && cd ..

#authorize the server key
touch .ssh/authorized_keys && sudo cat ${SSH_SERVER_KEY} >> .ssh/authorized_keys && sudo chmod 600 .ssh/authorized_keys 


sudo chown -R iaq-sensor: /home/iaq-sensor/.ssh


#download docker install script
curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh
sudo rm get-docker.sh




#reboot 
sudo sync && sudo /sbin/shutdown -r now

#nice work