#!/bin/bash


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi


#set docker non sudo account
sudo usermod -aG docker ${USER}
sudo usermod -aG docker ${USER}
groups ${USER}



#install docker compose
sudo apt-get -y install libffi-dev libssl-dev
sudo apt -y install python3-dev
sudo apt-get -y install python3 python3-pip
sudo pip3 install docker-compose


### Install telegraf
wget -qO- https://repos.influxdata.com/influxdb.key | sudo tee /etc/apt/trusted.gpg.d/influxdb.asc >/dev/null
source /etc/os-release
echo "deb https://repos.influxdata.com/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list




#reboot 
sudo reboot