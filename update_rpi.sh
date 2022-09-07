#!/bin/bash


read -p "This script will run commands on all specified raspi's, please type y, to confirm the execution." -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi


for port in 22200 22201 22202
do
	echo "Port: ${port}"
	ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no  -p ${port} pi@localhost << EOF
	hostname
	cd iaq-arrs
	git pull
	#--- here execute some commands to perform updates
	#--- end custom commands
	cd ..
	sudo rm ./status/configured.tmp
	sudo reboot
EOF
done