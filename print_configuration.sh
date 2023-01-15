#!/bin/bash

. ./configuration.sh


echo -n "version --"
cat /home/$(whoami)/iaq-arrs/version

echo -n "user --"
whoami

echo -n "hostname --"
hostname

echo -n "date --"
date

echo -n "ip --"
hostname -I | awk '{print $1}'

echo " --- connection --- "
iw dev
echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "



echo -n "docker status --"
systemctl status docker | grep "Active:" | grep -E --color 'Active|'

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo -n "setup_iaq_monitoring.service status --"
systemctl status setup_iaq_monitoring.service | grep "Active:\|Process:" | grep -E --color 'Active|'

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "


echo -n "collect_data.service status --"
systemctl status collect_data.service | grep "Active:\|Process:" | grep -E --color 'Active|'

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo -n "telegraf status --"
systemctl status telegraf | grep "Active:" | grep -E --color 'Active|'

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo -n "check_network.service status --"
systemctl status check_network.service | grep "Active:\|Process:" | grep -E --color 'Active|'

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo -n "check_network.timer status --"
systemctl status check_network.timer | grep "Active:\|Trigger:" | grep -E --color 'Active|'

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo " --- data collection configuration --- "
echo -n "measurement delta --"
echo ${MEASUREMENT_DELTA}
echo -n "building --"
echo ${BUILDING}
echo -n "network watchdog timer --"
echo ${WATCHDOG_TIMER}
echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "


echo -n "collect_data.service status --"
systemctl status collect_data.service | grep "Active:\|Process:" | grep -E --color 'Active|'

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "


echo -n "tunnel_to_ir.service status --"
systemctl status tunnel_to_ir.service | grep "Active:" | grep -E --color 'Active|'

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "