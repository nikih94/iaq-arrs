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
sudo apt-get update

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
sudo apt-get update
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
ExecStart=/bin/bash -c "runuser -l ${USER_ON_RASPI} -c "\""cd iaq-arrs ; pwd ; /usr/bin/git pull"\"""
ExecStart=/bin/bash -c "./data_acquisition/setup_scripts/setup.sh" 
ExecStart=/bin/bash -c "./data_acquisition/setup_scripts/enable.sh" 
ExecStart=/bin/bash -c "chmod 4755 /usr/sbin/reboot" 
ExecStop=/bin/bash -c "runuser -l ${USER_ON_RASPI} -c "\""./iaq-arrs/verify_status.sh"\"""

[Install]
WantedBy=multi-user.target
EOF



#move the servis to the correct DIR
cp ./configuration/setup_iaq_monitoring.service /etc/systemd/system/setup_iaq_monitoring.service

#The previous script will run only if the file /home/${USER_ON_RASPI}/status/configured.tmp exists
sudo runuser -l ${USER_ON_RASPI} -c "/usr/bin/mkdir /home/${USER_ON_RASPI}/status"

#enable the service
sudo systemctl enable setup_iaq_monitoring.service


#stop the service
sudo systemctl stop setup_iaq_monitoring.service




#Setup unit file that will run the network test
cat > configuration/check_network.service <<EOF
[Unit]
Description=Execute script to verify the network and reboot system if network is not working

[Service]
Type=oneshot
WorkingDirectory=/home/${USER_ON_RASPI}/iaq-arrs/
ExecStart=/bin/bash -c "./network_test.sh" 

EOF


#Setup unit file of the timer
cat > configuration/check_network.timer <<EOF
[Unit]
Description=Execute service to verify the network and reboot system if network is not working

[Timer]
Unit=check_network.service
OnCalendar=${WATCHDOG_TIMER}

[Install]
WantedBy=timers.target
EOF




##COPY SERVICES
cp ./configuration/check_network.timer /etc/systemd/system/check_network.timer
cp ./configuration/check_network.service /etc/systemd/system/check_network.service


##ENABLE SERVICES
#enable the service
sudo systemctl enable check_network.service
sudo systemctl enable check_network.timer


##  permissions
sudo chmod 775 network_test.sh



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
