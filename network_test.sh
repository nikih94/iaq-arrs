#!/bin/bash

i=0

ping -c4 8.8.8.8 > /dev/null

while [ $? != 0 ] && [ $i -lt 3 ]
do
   ((i=i+1))
   sleep 5
   ping -c4 8.8.8.8 > /dev/null
done



if [ $? != 0 ] 
then
	echo "No network... rebooting" 
  	sudo /sbin/shutdown -r now
fi


