
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

We would like to acknowledge the collegues Aleksandar Tošić[1,2], dr. Jernej Vičič[1], and prof. dr. Michael Mrissa[1,2] for the theoretical foundations, which are the basis for this implementation.
<br/>
<br/>
[1] University of Primorska, Faculty of Mathematics, Natural Sciences and Information Technologies
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

### Hardware requirements
 * 1 16Gb microSD Class 10 card
 * 1 raspberry Pi v4b + charger and case (extra hole to drill in the back of the red part over the SD card reader)
 * 1 Sensor

### Installation procedure
Install the Raspberry Pi imager program, start it.
Select "Use custom" and your raspi Pi image, to download [here](https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2022-04-07/2022-04-04-raspios-bullseye-arm64.img.xz)

Click on the "configuration" icon (a little wheel in the bottom right corner) it opens a new window where you will select "always use" and then set your keyboard layout and language, enable SSH with "use password authentication" and leave the other options by default.

Select your SD card and click "Write"
After the writing is successful, insert the SD card into your RPI.

Next, plug the sensor shown in the image below (Pins ...)

Plug a keyboard, a mouse, a screen, and start the RPI. You can now configure your wifi connection.
Once the wifi is connected, you are ready.
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
Configure and copy *To_copy_in_boot/wpa_supplicant.conf* in the *boot* folder of the SD card.



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
sudo umount /dev/mmcblk0p1
sudo umount /dev/mmcblk0p2
less /proc/mounts |grep mm
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
sudo umount /dev/mmcblk0p1
sudo umount /dev/mmcblk0p2
less /proc/mounts |grep mm
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











