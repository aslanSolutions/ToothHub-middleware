import paho.mqtt.client as mqtt
import time
import os


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connect" + str(rc))
    client.subscribe("middleware")
    client.publish("patient", "nawrooz")

client = mqtt.Client(client_id="middleware_side", userdata=None, protocol=mqtt.MQTTv5)
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

client.username_pw_set("group7", "Group777")
client.on_message = on_message
client.on_connect = on_connect

client.subscribe("patient")
client.publish("patient")

client.subscribe("dentist")
client.publish("dentist")

client.connect("0169ad6feac84c25b5b11b5157be1bd8.s2.eu.hivemq.cloud", 8883)

client.loop_start()
time.sleep(5)
client.disconnect()
