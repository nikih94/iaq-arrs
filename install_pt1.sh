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


#Install firewall
sudo apt-get -y install ufw
#deny all incoming traffic
sudo ufw default deny
# open port 22
sudo ufw allow 22 
#Do not port to access local DB (security is not ready)
#sudo ufw allow 3306 
sudo ufw enable

#set correct timezone
timedatectl set-timezone Europe/Rome

cd ~

#Set ssh keys
mkdir -p .ssh && sudo cat ssh_keys/id_rsa.pub > .ssh/id_rsa.pub && sudo cat ssh_keys/id_rsa > .ssh/id_rsa && cd .ssh/ && touch known_hosts && sudo chmod 400 id_rsa && sudo chmod 400 id_rsa.pub && sudo chmod 600 known_hosts && cd ..


#reboot 
sudo reboot

#nice work