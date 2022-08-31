#!/bin/bash


. ./configuration.sh


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi


#Setup unit file that will run sripts setup.sh and enable_iaq_monitoring.sh 
cat > ./configuration/setup_iaq_monitoring.service <<EOF
[Unit]
Description=Setup configuration and starts iaq monitoring
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/home/${USER_ON_RASPI}
ExecStart=/bin/bash -c "./iaq-arrs/setup.sh" 
ExecStart=/bin/bash -c "./iaq-arrs/enable_iaq_monitoring.sh" 
ExecStart=/bin/bash -c "./iaq-arrs/setup_latency_monitor.sh" 
ExecStop=/bin/bash -c "./iaq-arrs/verify_status.sh"

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


#open port for avahi
sudo ufw allow 59551  
sudo ufw allow 5353
sudo ufw allow 38304
sudo ufw allow 41357 
sudo ufw allow 33366
sudo ufw allow 50188


#open port for netserver
sudo ufw allow 12865
