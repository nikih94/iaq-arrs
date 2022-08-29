# tutorial here:
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

import random
import time

from paho.mqtt import client as mqtt_client


# verify connection
flag_connected = 0


broker = '88.200.63.216'
port = 8883
topic = "DAQ/"

client_id = 'mac-address'
username = 'Innorenew'
password = 'mrakova123'


def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0


def on_connect(client, userdata, flags, rc):
    global flag_connected
    if rc == 0:
        print("Connected to MQTT Broker!")
        flag_connected = 1
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client):
    msg_count = 0
    msg = "bananana"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1


# how it was used

# def do_something(sc):
#     global client
#     global count
#     print("Read data...")
#     # do your stuff
#     link_to_sensor.run_sync_client()
#     sensor_data = link_to_sensor.read_sensor()
#     # if not sensor_data: #check if it is empty
#     # if empty do something
#     if mqtt_client.flag_connected == 0:
#         client = mqtt_client.connect_mqtt()
#     mqtt_client.publish(client)
#     local_db_manager.save_to_local_db(count)
#     count = count + 1
#     s.enter(DELTA, 1, do_something, (sc,))
