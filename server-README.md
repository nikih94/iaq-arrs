
# Server installation and setup

### Influx DB

Install influxdb on the server.
Current influxDB version: *2.4.0*
<br>
Create users and create the following buckets: 
* iaq
* rpi_stats



## Reverse proxy

The reverse proxy is used to access sensors attached to remote networks. (mainly used for maintenance)

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




