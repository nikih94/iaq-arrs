#!/bin/bash

. ./configuration.sh

#Load the configuration variables
. ./iaq-arrs/configuration.sh


cd ./iaq-arrs/


# Colors
txt_red="\033[31m"    # Red
txt_green="\033[32m"  # Green
txt_yellow="\033[33m" # Yellow
txt_blue="\033[36m"   # Blue
txt_reset="\033[0m"   # Reset the prompt back to the default color


echo -n "user --"
whoami

echo -n "hostname --"
hostname

echo -n "date --"
date

echo -n "ip --"
hostname -I | awk '{print $1}'

echo " --- git branch --- "

git branch --show-current | grep production

if (($? > 0)); then
  echo -e "$txt_yellow"$(git branch --show-current)"$txt_reset"
else
  echo -e "$txt_green""production""$txt_reset"
fi


echo -n "version --"
git describe --tags


echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "


echo " --- connection --- "
/usr/sbin/iw dev
echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "



echo -n "docker status --"
systemctl status docker | grep "Active:" | grep -E --color 'Active|'
systemctl status docker | grep "Active:" | grep " active "

if (($? > 0)); then
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
else
  echo -e "$txt_green""\n 0K! all good \n""$txt_reset"
fi


echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo -n "setup_iaq_monitoring.service status --"
systemctl status setup_iaq_monitoring.service | grep "Active:\|Process:" | grep -E --color 'Active|'
systemctl status setup_iaq_monitoring.service | grep "Active:" | grep " failed "  

if (($? > 0)); then
  echo -e "$txt_green""\n 0K! all good \n""$txt_reset"
else
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
fi 

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "


echo -n "collect_data.service status --"
systemctl status collect_data.service | grep "Active:\|Process:" | grep -E --color 'Active|'
systemctl status collect_data.service | grep "Active:" | grep " active "

if (($? > 0)); then
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
else
  echo -e "$txt_green""\n 0K! all good \n""$txt_reset"
fi



echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo -n "telegraf status --"
systemctl status telegraf | grep "Active:" | grep -E --color 'Active|'
systemctl status telegraf | grep "Active:" | grep " active "

if (($? > 0)); then
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
else
  echo -e "$txt_green""\n 0K! all good \n""$txt_reset"
fi


echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo -n "check_network.service status --"
systemctl status check_network.service | grep "Active:\|Process:" | grep -E --color 'Active|'
systemctl status check_network.service | grep "Active:" | grep " inactive "

if (($? > 0)); then
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
else
  echo -e "$txt_green""\n 0K! all good \n""$txt_reset"
fi

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo -n "check_network.timer status --"
systemctl status check_network.timer | grep "Active:\|Trigger:" | grep -E --color 'Active|'
systemctl status check_network.timer | grep "Active:" | grep " active "

if (($? > 0)); then
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
else
  echo -e "$txt_green""\n 0K! all good \n""$txt_reset"
fi

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo " --- data collection configuration --- "
echo -n "measurement delta --"
echo ${MEASUREMENT_DELTA}
echo -n "building --"
echo ${BUILDING}
echo -n "network watchdog timer --"
echo ${WATCHDOG_TIMER}
echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "


echo -n "tunnel_to_ir.service status --"
systemctl status tunnel_to_ir.service | grep "Active:" | grep -E --color 'Active|'
systemctl status tunnel_to_ir.service | grep "Active:" | grep " active "

if (($? > 0)); then
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
else
  echo -e "$txt_green""\n 0K! all good \n""$txt_reset"
fi


echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo " --- overlay filesystem --- "


less /boot/cmdline.txt | grep "boot=overlay "



if (($? > 0)); then
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
else
  echo -e "$txt_green""\n 0K! all good \n""$txt_reset"
fi

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "

echo " --- WATCHDOG --- "



dmesg | grep "Set hardware watchdog to 14s."

if (($? > 0)); then
  echo -e "$txt_red""\n FAIL! There is a problem""$txt_reset"
else
  echo -e "$txt_green""\n Watchdog enabled !\n""$txt_reset"
fi

echo " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "