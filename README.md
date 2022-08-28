
<div align="center" >
    <h1 >
      <span style="color: #FF1493" >IAQ-ARRS</span>
    </h1>
    <h3>
        IoT indoor air quality monitoring platform
    </h3>
    <h3>
        <img alt="Up-famnit Logo" src="https://www.famnit.upr.si/img/UP_FAMNIT.png"  height ="100px">
        <img alt="InnoRenew Logo" src="https://innorenew.eu/app/themes/innorenew/assets/img/logo_color.svg" style="vertical-align: middle" height ="100px">
  </h3>
  </div>
  <div align="left">
    <br>
    <a href="#">
        <img alt="GPL License" src="https://img.shields.io/badge/license-GPL-brightgreen"/>
    </a><br>
    <a href="#">
        <img alt="ns-3 simulator" src="https://img.shields.io/badge/simulator-ns--3-brightgreen"/>
    </a>
</div>



## Table of contents
* [General info](#general-info)
* [Acknowledgments](#acknowledgments)
* [Technologies](#technologies)
* [Version](#version)
* [Documentation](#documentation) 
* [Installation and Setup](#installation-and-setup)

## General info
IoT indoor air quality monitoring platform


## Acknowledgments

We would like to acknowledge the collegues Aleksandar Tošić[1,2], dr. Jernej Vičič[1], and prof. dr. Mihael Mrissa[1,2] for the theoretical fundations, which are the basis for this implementation.
<br/>
<br/>
[1] University of Primorska Faculty of Mathematics, Natural Sciences and Information Technologies
<br/>
[2] Innorenew CoE 

## Technologies
The project builds on:
* nsnam ns-3: 3.35
* libsodium: 1.0.18-1
* protobuf: 3.19.1
	
## Version

Version 1.0


## Documentation


  
## Installation and Setup

### Server

#### Influx DB

#### Reverse proxy

The reverse proxy is used to access Sensors attached to remote networks, mainly for maintainance.

##### Create the Sensor user on the Server

```
sudo useradd -m raspi
```
Disable the login shell for the Sensor user (raspi)

```
sudo usermod raspi -s /sbin/nologin
```

##### Configure permissions for SSH connection on the Sensor user

Edit the config file:

```
sudo nano /etc/ssh/sshd_config
```

Paste the following at the end of the config:

```
Match User raspi
        AllowTcpForwarding yes
                PermitOpen localhost:22222 localhost:22223
        X11Forwarding no
        PermitTunnel no
        GatewayPorts no
        AllowAgentForwarding no
        PasswordAuthentication no
```

Pay attention, the PermitOpen clause allows TCP forwarding only on the specified ports, you need to activate this for all the used ports
<br>
<br>
Reload the sshd 

```
sudo systemctl reload sshd
```

##### Setup SSH tunnel on Sensors

Look at the section: [SSH tunnel](#ssh-tunnel)


### Sensors




#### SSH tunnel

##### Generate SSH keys

Run the following command and press always enter
```
ssh-keygen
```

Follow the following [guide](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server) to copy the ssh public key to the authorized_keys directory on the server.
<br>

remember that you must create the .ssh directory on the server. The following commands may be useful:


```
sudo mkdir /home/raspi/.ssh
sudo su
cat raspi_public_key >>  /home/raspi/.ssh/authorized_keys
```


##### Create the SSH tunnel with systemd

Setup a systemd unit file, to maintain a persistent tunnel to the IR server. In the following the unit file template, this is generated by the script *setup.sh*

```
[Unit]
Description=Setup a secure tunnel to IR
After=network-online.target

[Service]
User=${USER}
ExecStart=/usr/bin/ssh -NT -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -R ${SERVER_PORT}:localhost:${RASPI_PORT} ${SENSOR_USER}@${SERVER_IP}

# Restart every >2 seconds to avoid StartLimitInterval failure
RestartSec=5
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable the tunnel_to_ir service: `sudo systemctl enable tunnel_to_ir.service` (enabled by the script *enable_iaq_monitoring.sh*)


#### Telegraf - status monitoring

Configure telegraf:
* First setup influxDB on the server
* Login to influxDB -> Load Data -> TELEGRAF -> Create Configuration -> (setup appropriately)
* Download the configuration file
* uncomment the line `insecure_skip_verify = false`
* move telegraf configuration in `/etc/telegraf/telegraf.conf`
* Copy the telegraf token from influxdb into: `echo "INFLUX_TOKEN=MY-TOKEN" > /etc/default/telegraf`
* Enable the telegraf service: `sudo systemctl enable telegraf.service` (enabled by the script *enable_iaq_monitoring.sh*)



