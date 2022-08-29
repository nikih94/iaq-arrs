
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

remember that you must create the .ssh directory on the server. The following commands may be useful:


```
sudo mkdir /home/raspi/.ssh
sudo su
cat raspi_public_key >>  /home/raspi/.ssh/authorized_keys
```


#### Install the application

Log into the raspi and perform the following

##### Install git and download the application

```
sudo apt-get install git
git clone https://github.com/nikih94/iaq-arrs/
```

##### SSH keys

Move the SSH keys (private key: **id_rsa** public key: **id_rsa.pub**) into `ssh_keys`

##### Configuration file


The sensor is configured by setting variables in the file *configuration_template.sh* to the appropriate values. The file must be then renamed to: *configuration.sh*
All variables are explained with comments.

##### Installation scripts

Run the two installation scripts respectively *install_pt1.sh* and *install_pt2.sh* the system will reboot between scripts.

##### DD command to replicate the system to all sensors

```
the dd command
```

The following sections must be performed on each raspi

##### Adjust configuration file

Alter the configuration file by setting the **SENSOR_HOSTNAME** and **BUILDING** building variable.

##### Setup script

Run the script *setup.sh* that will generate configuration files in the folder *configuration*

##### Enable application

Run the script *enable_iaq_monitoring.sh* that will move configuration files in appropriate postions, set permissions and enable services.


##### Sensors are now ready










