#!/bin/bash

##disable power management of wireless
/sbin/iwconfig wlan0 power off

i=0

ping -c4 8.8.8.8 > /dev/null

while [ $? != 0 ] && [ $i -lt 3 ]
do
   ((i=i+1))
   killall dhclient
   sleep 1
   /sbin/ifconfig wlan0 down 
   sleep 10
   /sbin/ifconfig wlan0 up
   sleep 10
   ping -c4 8.8.8.8 > /dev/null
done



if [ $? != 0 ] 
then
	echo "No network... rebooting" 
   ## ATTENTION 
  	#sudo sync && sudo /sbin/shutdown -r now
fi


