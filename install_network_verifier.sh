#!/bin/bash


#Load the configuration variables
. ./configuration.sh


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi



#Setup unit file that will run the network test
cat > configuration/check_network.service <<EOF
[Unit]
Description=Execute script to verify the network and reboot system if network is not working
Wants=check_network.timer

[Service]
Type=oneshot
WorkingDirectory=/home/${USER_ON_RASPI}/iaq-arrs/
ExecStart=/bin/bash -c "./network_test.sh" 

EOF


#Setup unit file of the timer
cat > configuration/check_network.timer <<EOF
[Unit]
Description=Execute service to verify the network and reboot system if network is not working
Requires=check_network.service

[Timer]
Unit=check_network.service
OnBootSec=15min
OnCalendar=*:0/15

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
