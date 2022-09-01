#!/bin/bash


#check if the configuration is already updated

if [[ -f "../status/configured.tmp" ]]
then
    echo "System already configured."
    exit 0
fi
echo "Pulling new version from github"


if git pull 2>/dev/null | grep -q "Already up to date."
then 
   echo "Already up to date."
else
   echo "Updated, now rebooting it worked";
fi



#Setup unit file that will run sripts setup.sh and enable_iaq_monitoring.sh 
cat > configuration/gitpull.service <<EOF
[Unit]
Description=gitpull
After=network-online.target

[Service]
Type=oneshot
User=pi
WorkingDirectory=/home/pi/iaq-arrs
ExecStart=/bin/bash -c "./try_update.sh"


[Install]
WantedBy=multi-user.target
EOF

