#!/bin/bash

#check if the configuration is already updated
# when executing this i'm in the home dir of the user!

if [[ -f "./status/configured.tmp" ]]
then
    echo "System already configured."
    exit 0
fi
echo "The system was reconfigured, now rebooting"

touch ./status/configured.tmp

sync && /sbin/shutdown -r now
