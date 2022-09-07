#!/bin/bash



for port in 22202
do
	ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no  -p ${port} pi@localhost << EOF
	whoami
	cd iaq-arrs
	git pull
	#--- here execute some commands to perform updates
	#--- end custom commands
	cd ..
	sudo rm ./status/configured.tmp
	sudo reboot
EOF
done