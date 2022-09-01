#!/bin/bash


#check if the configuration is already updated

if [[ -f "../status/configured.tmp" ]]
then
    echo "System already configured."
    #exit 0
fi
echo "Pulling new version from github"


if git pull 2>/dev/null | grep -q "Already up to date."
then 
   echo "NOT updated";
else
   echo "Updated yeah";
fi

