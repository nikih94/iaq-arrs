
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

We would like to acknowledge the collegues Aleksandar Tošić[1,2], dr. Jernej Vičič[1], and prof. dr. Michael Mrissa[1,2] for the theoretical fundations, which are the basis for this implementation.
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

##### Setup SSH tunnel on Sensors

Look at the section: [SSH tunnel](#ssh-tunnel)


### Sensors

#### Install OS and setup basics

Install RaspiOS with raspi-imager.
* Mandatory: arm64 image.
* Use the image *2022-04-04-raspios-bullseye-arm64-lite.img.xz*

##### Allow UART communication

Copy the script *To_copy_in_boot/my_config.txt* in the *boot* foler of the SD card

##### Setup SSH and WiFi

Copy *To_copy_in_boot/ssh* in the *boot* foler of the SD card.<br>
Configure and copy *To_copy_in_boot/wpa_supplicant.conf* in the *boot* foler of the SD card.



#### SSH tunnel

##### Generate SSH keys

Run the following command and press always enter
```
ssh-keygen
```

Store the SSH keys (private key: **id_rsa** public key: **id_rsa.pub**) for later



Follow the following [guide](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server) to copy the ssh public key to the authorized_keys directory on the server.
<br>

You must create the .ssh directory on the server. You must set ownership of .ssh and its files to the raspi user. The following commands may be useful:


```
sudo mkdir /home/raspi/.ssh
sudo su
cat raspi_public_key >>  /home/raspi/.ssh/authorized_keys
```


#### Install the application

Log into the raspi and perform the following


##### SSH keys

Move the SSH keys (private key: **id_rsa** public key: **id_rsa.pub**) into `ssh_keys`
<br>
Execute the following commands:
  
  
  
```
mkdir -p /home/pi/.ssh && sudo cat ssh_keys/id_rsa.pub > /home/pi/.ssh/id_rsa.pub && sudo cat ssh_keys/id_rsa > /home/pi/.ssh/id_rsa && cd .ssh/ && touch known_hosts && sudo chmod 400 id_rsa && sudo chmod 400 id_rsa.pub && sudo chmod 600 known_hosts && cd ..

```


##### Install git and download the application

```
sudo apt-get install git
git clone https://github.com/nikih94/iaq-arrs
```


##### Configuration file


The sensor is configured by setting variables in the file *configuration_template.sh* to the appropriate values. The file must be then renamed to: *configuration.sh*
All variables are explained with comments.

##### Set the raspi password

Use the `passwd` command to set a new password

##### Installation scripts

Run the two installation scripts respectively *install_pt1.sh* and *install_pt2.sh* the system will reboot between scripts.
<br>
If *install_pt1.sh* does not work due to **apt update** not working, run the following commands:
```
sudo rm -r /var/lib/apt/lists/*
sudo apt update
```
Then re-run *install_pt1.sh*.


##### DD command to replicate the system to all sensors

Do next steps:
* Insert the SD card in the laptop.
* The SD card must NOT be mounted
* List all attacheed devices `sudo fdisk -l`
* Use the **dd** command to create a new image

```
sudo umount /dev/mmcblk0 
sudo dd if=/dev/mmcblk0 of=/home/niki/Desktop/ARRS/production_images/test.img
```

*Requires 3.5mins*

<br>
Shrink image using [PiShrink](https://github.com/Drewsif/PiShrink)

```
sudo pishrink.sh /home/niki/Desktop/ARRS/production_images/test.img
```

##### The following sections must be performed on each raspi

Insert empty SD in laptop. Run the command to copy the image to the sd:

```
sudo umount /dev/mmcblk0 
sudo dd if=/home/niki/Desktop/ARRS/production_images/test.img of=/dev/mmcblk0
```
*Requires 5mins*


<br>

Insert the SD and perform the following:

###### Schedule a re-setup

Delete the file /home/pi/status/configured.tmp
<br>

###### Adjust configuration file

Alter the configuration file by setting the **SENSOR_HOSTNAME** and **BUILDING** and **SERVER_PORT** building variable.

###### Set the wireless supplicant

Copy a new *wpa_supplicant.conf* file into boot

###### Sensors are now ready











