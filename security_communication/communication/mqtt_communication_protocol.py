from .communication_protocol import CommunicationProtocol
import json
import copy
import random
import string
import mimetypes
import http.client
from enum import Enum
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


def on_publish(client, userdata, mid):
    client.disconnect()
    client.loop_stop()

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
    else:
        print("Bad connection Returned code=", rc)
        client.bad_connection_flag=True

def on_subscribe(client, obj, mid, granted_qos):
    pass #print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    # print("on_message:", end=': ')
    # print(msg)
    # print("on message callback called...\n")
    pass

class MQTTCommunicationProtocol(CommunicationProtocol):

    def __init__(self, config, send_callback = None, receive_callback = None):
        super(MQTTCommunicationProtocol, self).__init__(config, send_callback, receive_callback)
        self.brokers = self.config["bootstrap_servers"]
        self.topic = self.config["topic"]
        self.time_interval = self.config["time_interval"]

    def _send_to_single_broker(self, broker, data):
        try:
            mqttc = mqtt.Client()
            if broker["user"] and broker["password"] :
                mqttc.username_pw_set(broker['user'], broker['password'])
            mqttc.on_publish = on_publish
            mqttc.on_connect = on_connect
            mqttc.on_message = on_message

            try:
                mqttc.loop_start()
                mqttc.connect(broker['ip_address'], broker['port']) #connect to broker
            except:
                #print("connection to {}:{} failed".format(broker['ip_address'], broker['port']))
                raise Exception("not connected")

            msg = {}
            msg["timestamp"] = data["msg"]["timestamp"] * 1000
            msg["sensor_id"] = data["msg"]["custom_id"]
            msg["value"] = data["msg"]["values"]
            mqttc.subscribe(self.topic)
            mqttc.publish(self.topic, json.dumps(msg), qos=1)

        except Exception as e:
            print(e)
            print("MQTT: something went wrong while sending message")

    def send(self, data, callback = None):
        if not callback:
            callback = self.send_callback

        for broker in self.brokers:
            self._send_to_single_broker(broker, data)

        if callback:
            callback()

    def receive(self, callback = None):
        pass
