import paho.mqtt.client as mqtt
import certifi
import time
import json
from datetime import datetime
from config import MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PW, MQTT_SOURCE

def on_connect(client, userdata, flag, rc):
    print("Successfully connected to MQTT server!")

def make_message(data):
    msg = json.loads(data)
    msg["type"] = "data"
    msg["source"] = MQTT_SOURCE

    return json.dumps(msg)

def mqtt_init():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.tls_set(certifi.where())
    client.username_pw_set(MQTT_USER, MQTT_PW)
    client.connect(MQTT_HOST, MQTT_PORT)
    
    return client 
