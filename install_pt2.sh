#!/bin/bash


#Load the configuration variables
. ./configuration.sh


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

#update apt
sudo apt update

#set docker non sudo account
sudo usermod -aG docker ${USER_ON_RASPI}
sudo usermod -aG docker ${USER_ON_RASPI}
groups ${USER_ON_RASPI}



#install docker compose
sudo apt-get -y install libffi-dev libssl-dev
sudo apt -y install python3-dev
sudo apt-get -y install python3 python3-pip
sudo pip3 install docker-compose


### Install telegraf
wget -qO- https://repos.influxdata.com/influxdb.key | sudo tee /etc/apt/trusted.gpg.d/influxdb.asc >/dev/null
source /etc/os-release
echo "deb https://repos.influxdata.com/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
sudo apt-get -y install telegraf



#create the configuration dir if not exist
mkdir -p configuration


#Setup unit file that will run sripts setup.sh and enable_iaq_monitoring.sh 
cat > configuration/setup_iaq_monitoring.service <<EOF
[Unit]
Description=Setup configuration and starts iaq monitoring
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/home/${USER_ON_RASPI}/iaq-arrs/
ExecStartPre=/bin/bash -c "./try_update.sh"
ExecStart=/bin/bash -c "./data_acquisition/setup_scripts/setup.sh" 
ExecStart=/bin/bash -c "./data_acquisition/setup_scripts/enable.sh" 
ExecStop=/bin/bash -c "./verify_status.sh"

[Install]
WantedBy=multi-user.target
EOF

#move the servis to the correct DIR
cp ./configuration/setup_iaq_monitoring.service /etc/systemd/system/setup_iaq_monitoring.service

#The script will run only if the file /home/${USER_ON_RASPI}/status/configured.tmp exists
mkdir -p /home/${USER_ON_RASPI}/status

#enable the service
sudo systemctl enable setup_iaq_monitoring.service

#stop the service
sudo systemctl stop setup_iaq_monitoring.service

#remove the configured file if it exists, so at the next boot, the system will be reconfigured
sudo rm /home/${USER_ON_RASPI}/status/configured.tmp



####
#
#   ENABLE SERVICES
#
####


sudo enable docker-compose daemon
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
