# tutorial here:
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
import pymysql
import paho.mqtt.subscribe as subscribe
import json
import sys

DB_HOST = "88.200.63.216"
DB_DATABASE = "SensorDB"
DB_USERNAME = "Innorenew"
DB_PASSWORD = "mrakova123"

MQTT_BROKER = "88.200.63.216"
MQTT_PORT = 8883
MQTT_USERNAME = "Innorenew"
MQTT_PASSWORD = "mrakova123"


def IAQinsert(db, source_p, meta_sn_p, meta_fw_p, meta_ip_p, meta_rssi_p, meta_name_p, meta_uptime_p, T_p, RH_p, CO2_p, p_p, ambient_light_p, VOC_index_p, PM1_p, PM2_5_p, PM4_p, PM10_p):
    try:
        cursor = db.cursor()

        sql = "INSERT INTO mrakova VALUES ('{source}','{meta_sn}','{meta_fw}','{meta_ip}',{meta_rssi},'{meta_name}',{meta_uptime},{T},{RH},{CO2},{p},{ambient_light},{VOC_index},{PM1},{PM2_5},{PM4},{PM10},NOW())".format(
            source=source_p,
            meta_sn=meta_sn_p,
            meta_fw=meta_fw_p,
            meta_ip=meta_ip_p,
            meta_rssi=meta_rssi_p,
            meta_name=meta_name_p,
            meta_uptime=meta_uptime_p,
            T=T_p,
            RH=RH_p,
            CO2=CO2_p,
            p=p_p,
            ambient_light=ambient_light_p,
            VOC_index=VOC_index_p,
            PM1=PM1_p,
            PM2_5=PM2_5_p,
            PM4=PM4_p,
            PM10=PM10_p,
        )
        cursor.execute(sql)
        db.commit()
        db.close()
    except:
        # Rollback in case there is any error
        print('Error during the insertion with the following sql command: \n'+sql)
        sys.stdout.flush()
        db.rollback()


def MRAKOVAJSONParser(message):
    print("Message arrived from the topic:"+message.topic)
    sys.stdout.flush()
    data = json.loads(message.payload, strict=False)
    source = message.topic
    meta_sn = data['meta']['sn']
    meta_fw = data['meta']['fw']
    meta_ip = data['meta']['ip']
    meta_rssi = data['meta']['rssi']
    meta_name = data['meta']['name']
    meta_uptime = data['meta']['uptime']
    T = data['T']
    RH = data['RH']
    CO2 = data['CO2']
    p = data['p']
    ambient_light = data['ambient_light']
    VOC_index = data['VOC_index']
    PM1 = data['PM1']
    PM2_5 = data['PM2_5']
    PM4 = data['PM4']
    PM10 = data['PM10']
    db = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
    IAQinsert(db, source, meta_sn, meta_fw, meta_ip, meta_rssi, meta_name,
              meta_uptime, T, RH, CO2, p, ambient_light, VOC_index, PM1, PM2_5, PM4, PM10)
