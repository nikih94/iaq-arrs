#!/bin/bash


. ./configuration.sh


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

#check if the configuration is already updated

if [[ -f "../status/configured.tmp" ]]
then
    echo "System already configured."
    exit 0
fi
echo "Start system configuration"



####
#
#   SETUP THE CONFIGURATION
#
####





cat >> ./configuration/configuration.ini <<EOF


[network_latency]
measurement_delta=${LATENCY_DELTA}
central_server_ip=${NETPERF_IP}
latency_test_timeout=60
latency_bucket=network_latency
EOF


####
#
#   GENERATE THE UNIT FILE FOR LATENCY MONITORING
#
####


cat > ./configuration/latency_monitor.service <<EOF
[Unit]
Description=Collect data from IAQ sensors and send to central DB
Requires=docker.service
PartOf=docker.service
After=setup_iaq_monitoring.service

[Service]
User=${USER_ON_RASPI}
Restart=always
Group=docker
RestartSec=180
WorkingDirectory=/home/${USER_ON_RASPI}/iaq-arrs/latency_monitor/docker/
# Shutdown container (if running) when unit is started
ExecStartPre=/usr/local/bin/docker-compose -f docker-compose.yml down
# Start container when unit is started
ExecStart=/usr/local/bin/docker-compose -f docker-compose.yml up
# Stop container when unit is stopped
ExecStartPost=/usr/local/bin/docker-compose -f docker-compose.yml down
# Rebuild container when unit is stopped
ExecStop=/usr/local/bin/docker-compose -f docker-compose.yml build

[Install]
WantedBy=multi-user.target
EOF



#copy the configuration file
cp ./configuration/configuration.ini ./latency_monitor/configuration.ini


#move the unit file
cp ./configuration/latency_monitor.service /etc/systemd/system/latency_monitor.service


####
#
#   ENABLE SERVICES 
#
####

sudo systemctl enable latency_monitor.service



echo "Latency monitoring configured"