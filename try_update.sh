#!/bin/bash


#check if the configuration is already updated

if [[ -f "../status/configured.tmp" ]]
then
    echo "System already configured."
    exit 0
fi
echo "Pulling new version from github"

pwd

git pull


