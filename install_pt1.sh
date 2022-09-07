#!/bin/bash


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


#download docker install script
curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh
sudo rm get-docker.sh



#set correct timezone
timedatectl set-timezone Europe/Rome

cd ~

#Set ssh keys
mkdir -p .ssh && sudo cat ssh_keys/id_rsa.pub > .ssh/id_rsa.pub && sudo cat ssh_keys/id_rsa > .ssh/id_rsa && cd .ssh/ && touch known_hosts && sudo chmod 400 id_rsa && sudo chmod 400 id_rsa.pub && sudo chmod 600 known_hosts && cd ..

#authorize the server key
cd .ssh && touch authorized_keys && sudo cat server.pub >> /home/pi/.ssh/authorized_keys && sudo chmod 600 authorized_keys && cd ..

#reboot 
sudo reboot

#nice work