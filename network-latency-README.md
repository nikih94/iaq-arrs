# Network latency plug-in

The network latency plug-in allows to measure the latency of the communication among devices located in the same LAN network. The plug-in was used in a gateway location optimization study. 

## Description

The plugin relies on the [Avahi](https://wiki.archlinux.org/title/avahi) (zeroconf) implementation for service discovery. Devices are advertising that they have the network latency plug-in enabled, and are reachable for devices in the same LAN network. 
Devices are then periodically measuring the latency among all network latency enabled devices using the [netperf](https://linux.die.net/man/1/netperf) benchmark tool. Also the latency device-server is measured and all data is sent to the server.


## Requirements

The device must be configured as described [here](README.md).
<br>
An influxdb server configured as described [here](server-README.md).

### Server - additional configuration

The influxdb server must have a bucket named *network_latency*
<br>
To allow measure latency from sensors to the server, the netperf package must be installed `sudo apt-get install netperf` and the netserver must be running on port 12865.

```netserver -4```

Please ensure firewall rules allow the correct functioning.
Netserver uses also other ports beside the 12865!!!


### Devices - additional configuration

If the *network_latency* component is required, it must be installed by running the script *install_latency_monitor.sh*

