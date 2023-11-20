import json
import paho.mqtt.client as mqtt
import time

primary_broker_url = "0169ad6feac84c25b5b11b5157be1bd8.s2.eu.hivemq.cloud"
backup_broker_url = ""

current_broker_url = primary_broker_url

middleware_client = mqtt.Client(client_id="middleware_side", protocol=mqtt.MQTTv311)
middleware_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        client.subscribe("patient")
        client.subscribe("dentist")
    else:
        print("Connection failed with code " + str(rc))
        if current_broker_url == primary_broker_url:
            print("Switching to backup broker")
            client.reinitialise()
            client.connect(backup_broker_url, port=8883)
            current_broker_url = backup_broker_url

def on_message(client, userdata, msg):
    try:
        print("Message received: ", msg.topic, ", ", msg.payload.decode("utf-8"))
        
        if msg.topic == "patient":
            middleware_client.publish("dentist", msg.payload, qos=1)

        elif msg.topic == "dentist":
            pass

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

middleware_client.on_connect = on_connect
middleware_client.on_message = on_message
middleware_client.username_pw_set("group7", "Group777")

middleware_client.connect(primary_broker_url, port=8883)

middleware_client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting from the broker")
    middleware_client.disconnect()
    middleware_client.loop_stop()
