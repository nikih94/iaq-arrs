#!/bin/sh -e
echo "starting"

#Start netserver
/usr/local/bin/netserver -4

echo "host mac address"
cat /sys/class/net/wlan0/address
#cat /sys/class/net/wlp0s20f3/address

#store the raspi net device
mac=$( cat /sys/class/net/wlan0/address )
#mac=$( cat /sys/class/net/wlp0s20f3/address )
# create the service
service="<!DOCTYPE service-group SYSTEM \"avahi-service.dtd\"><service-group><name replace-wildcards=\"no\">network-latency</name><service protocol=\"ipv4\"><type>_http._tcp</type><port>12865</port><txt-record>$mac</txt-record></service></service-group>"


echo $service > /etc/avahi/services/network-latency.service

#tryin to kill stuff but didn't work 
#kill the dbus and avahi-daemon if they esist
#kill $(ps aux | grep '[d]bus' | awk '{print $2}')
#kill $(ps aux | grep '[a]vahi-daemon' | awk '{print $2}')
#avahi-daemon -k






FILE=/run/dbus/dbus.pid

if [ -f "$FILE" ]; then
    echo "dbus exists" 
    #end the program, will be restarted by systemd with new container
else
    echo "Starting latency monitor"
    #start the avahi -daemon
    dbus-daemon --system
    avahi-daemon --no-chroot --daemonize
    cd /arrs_or/latency_monitor/
    echo "Start main program"
    #python3 hello.py
    python3 main.py
    echo "Program died"
fi


