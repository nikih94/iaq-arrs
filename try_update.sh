#!/bin/bash

# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

#check if the configuration is already updated

if [[ -f "./status/configured.tmp" ]]
then
    echo "System already configured."
    exit 0
fi
echo "Pulling new version from github"

git pull 


