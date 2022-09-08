
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
        <img alt="docker" src="https://img.shields.io/badge/docker-enabled-blue"/>
    </a>
	<br>
    <a href="#">
        <img alt="influx" src="https://img.shields.io/badge/influxdb-timeseries-orange"/>
    </a>
</div>



# Table of contents
* [General info](#general-info)
* [Acknowledgments](#acknowledgments)
* [Technologies](#technologies)
* [Version](#version)
* [Documentation](#documentation) 
* [Installation and Setup](#installation-and-setup)

# General info
IoT indoor air quality monitoring platform


# Acknowledgments

We would like to acknowledge the collegues Aleksandar Tošić[1,2], dr. Jernej Vičič[1], and prof. dr. Michael Mrissa[1,2] for the theoretical fundations, which are the basis for this implementation.
<br/>
<br/>
[1] University of Primorska Faculty of Mathematics, Natural Sciences and Information Technologies
<br/>
[2] Innorenew CoE 

# Technologies
The project builds on:
* influxdb: 2,4,0
* docker: 20.10.17
	- linux-alpine: 3.15
* netperf: 2.7
* avahi: 0.8
* raspberryOs: debian-11-bullseye
* python
* mariadb: 10.4.24
* minimalmodbus
	
# Version

Version 1.0


# Documentation

## TO-DO


# Server installation and setup

### Influx DB

Install influxdb on the server. Current influxDB version: *2.4.0*
<br>
Create users and crete the following buckets: 
* iaq
* network_latency
* rpi_stats



## Reverse proxy

The reverse proxy is used to access Sensors attached to remote networks. (mainly used for maintainance)

<br>
Create the Sensor user on the Server

```
sudo useradd -m raspi
```
Disable the login shell for the Sensor user (raspi)

```
sudo usermod raspi -s /sbin/nologin
```

Configure permissions for SSH connection on the Sensor user by editing the config file

```
sudo nano /etc/ssh/sshd_config
```

Paste the following at the end of the config:

```
Match User raspi
        AllowTcpForwarding yes
                PermitOpen localhost:22200 localhost:22201 localhost:22202 localhost:22203 localhost:22204  localhost:22205 localhost:22206 localhost:22207 localhost:22208 localhost:22209 localhost:22210 localhost:22211 localhost:22212 localhost:22213 localhost:22214 localhost:22215 localhost:22216 localhost:22217 localhost:22218 localhost:22219 localhost:22220 localhost:22221 localhost:22222 localhost:22223 localhost:22224 localhost:22225 localhost:22226 localhost:22227 localhost:22228 localhost:22229 localhost:22230 localhost:22231 localhost:22232 localhost:22234 localhost:22235 localhost:22236 localhost:22237 localhost:22238 localhost:22239 localhost:22240
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

### Setup SSH tunnel on Sensors

Look at the section: [SSH tunnel](#ssh-tunnel)

## Update raspi's remotely

This will allow to run a script that will ssh raspberrys and will run commands on them. (Mainly used for updates or fixes).

### Generate ssh keys of the server

Run the following command and press always enter. The keys will be stored in the *.ssh* folder in the home directory. If the folder does not exist create the folder `sudo mkdir .ssh`
```
ssh-keygen
```

Move the server's ssh public key to the file *authorized_keys* on the raspi. Explained [here](#move-server-key-to-raspi)


### Update


Run the command:


```
cat update-command-list.txt | parallel-ssh -o out/  -h all-rpi-host-file.txt -X '-o StrictHostKeyChecking=no' -X '-o PasswordAuthentication=no'  --send-input
```

The file *update-command-list.txt* contains commands that will be executed on sensor specified in the file *all-rpi-host-file.txt*.
<br>
An example of the file *update-command-list.txt*:
```
echo "Updating raspi"
hostname
pwd
cd iaq-arrs
git pull
#--- here execute some commands to perform updates
#--- end custom commands
cd ..
sudo rm ./status/configured.tmp
sudo shutdown -r
echo "Now rebooting"
```

An example of the file *all-rpi-host-file.txt*:

```
pi@localhost:22200
pi@localhost:22201
pi@localhost:22202
pi@localhost:22203
pi@localhost:22204
```




## Network latency

To allow measure latency from sensors to serve, the netperf package must be installed `sudo apt-get install netperf` and the netserver must be running on port 12865.

```netserver -4```

Please ensure firewall rules allow the correct functioning.
Netserver uses also other ports beside the 12865!!!



# Raspi installation

## Install OS and setup basics

Install RaspiOS with raspi-imager.
* Mandatory: arm64 image.
* Use the image *2022-04-04-raspios-bullseye-arm64-lite.img.xz* OR *2022-04-04-raspios-bullseye-arm64.img.xz*

### Allow UART communication

Copy the script *To_copy_in_boot/my_config.txt* in the *boot* foler of the SD card.
<br>
This script will enable the UART communication and disable some things that may disturb the communication.

### Setup SSH and WiFi

Copy *To_copy_in_boot/ssh* in the *boot* foler of the SD card.<br>
Configure and copy *To_copy_in_boot/wpa_supplicant.conf* in the *boot* foler of the SD card.



## SSH tunnel


Run the following command to generate ssh keys and press always enter

```
ssh-keygen
```

Store the SSH keys (private key: **id_rsa** public key: **id_rsa.pub**) in the folder *ssh_keys*. The folder must locate in the home directory of the user of the raspi.

### Move public key to the server

Follow the following [guide](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server) to copy the ssh public key to the authorized_keys directory on the server.
<br>

You must create the .ssh directory on the server. You must set ownership of .ssh and its files to the raspi user. The following commands may be useful:


```
sudo mkdir /home/raspi/.ssh
sudo su
cat raspi_public_key >>  /home/raspi/.ssh/authorized_keys
```

### Move server key to raspi

Copy the server public key to the *ssh_keys* folder on the raspi. The server's ssh public key must be named *server.pub*. The folder *ssh_keys* must locate in the home directory of the user of the raspi.


## Install the application

Please insert the SD card in the raspi and start the system.
Enter the user shell in some way.

<br>

Run the command to set a new password: `passwd`

<br>

Install git and download the application

```
sudo apt-get install git
git clone https://github.com/nikih94/iaq-arrs
```


### Configuration file 


The sensor is configured by setting variables in the file *configuration_template.sh* to the appropriate values. The file must be then renamed to: *configuration.sh*
All variables are explained with comments.



### Installation scripts

Run the two installation scripts respectively *install_pt1.sh* and *install_pt2.sh* the system will reboot between scripts.
<br>
If *install_pt1.sh* does not work due to **apt update** not working, run the following commands:
```
sudo rm -r /var/lib/apt/lists/*
sudo apt update
```
Then re-run *install_pt1.sh*.
<br>
After running the script *install_pt2.sh* check that telegraf was installed!! If it was not installed run the command `sudo apt-get update` and re-run the script *install_pt2.sh*.

### Installation of *network_latency* component

If the *network_latency* component is required, it must be installed at this step.
Run the script *install_latency_monitor.sh*
<br>
For the correct functioning of the *network_latency* component the *netserver* must be running on the server. Please check this section to enable: [netserver](network-latency)

## Raspi replication

### Base image creation

To perform this section, you must have an SD card that was prepared following the steps in [raspi installation](raspi-installation)
<br>

#### Schedule a re-setup

Delete the file /home/pi/status/configured.tmp
```
sudo rm /home/pi/status/configured.tmp
```
This will schedule a reboot and resetup when at the next system startup.

#### Create the base image

Perform the following:
* Insert the SD card in the laptop.
* The SD card must NOT be mounted
* List all attacheed devices `sudo fdisk -l`
* Use the **dd** command to create a new image

```
sudo umount /dev/mmcblk0 
sudo dd if=/dev/mmcblk0 of=./images/test.img
```

*Requires more or less 3.5mins*

<br>
Shrink image using [PiShrink](https://github.com/Drewsif/PiShrink)

```
sudo pishrink.sh -r ./images/test.img ./images/shrinked_test.img
```

## Image replication

Insert SD to overwrite in PC. Ensure, that the SD is not mounted. Run the command to copy the image to the sd:

```
sudo umount /dev/mmcblk0 
sudo dd if=./images/shrinked_test.img of=/dev/mmcblk0
```
*Requires more or less 10mins*

#### Setup the clone image

Mount the SD and perform the following:
<br>

Alter the configuration file by setting the **SENSOR_HOSTNAME** and **BUILDING** and **SERVER_PORT** building variable.


Create the *wpa_supplicant.conf* and copy, set it correctly and it into the *boot* folder.
<br>
**The clone is now ready**
<br>
Insert the SD card into the raspberry











