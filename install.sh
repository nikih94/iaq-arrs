#!/bin/bash


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi


#update system
sudo apt-get update
sudo apt-get upgrade

#then setup UART on raspi4
sudo raspi-config nonint do_serial 1
sudo cp /boot/my_config.txt /boot/config.txt


#download docker install script
curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh
sudo rm get-docker.sh

#set docker non sudo account
sudo usermod -aG docker ${USER}
sudo usermod -aG docker ${USER}
groups ${USER}



#install docker compose
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip
sudo pip3 install docker-compose


### Install telegraf
wget -qO- https://repos.influxdata.com/influxdb.key | sudo tee /etc/apt/trusted.gpg.d/influxdb.asc >/dev/null
source /etc/os-release
echo "deb https://repos.influxdata.com/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update && sudo apt-get install telegraf


#reboot 
sudo reboot