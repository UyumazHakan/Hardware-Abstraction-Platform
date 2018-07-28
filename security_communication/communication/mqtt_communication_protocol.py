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

class MQTTCommunicationProtocol(CommunicationProtocol):

    def __init__(self, config, send_callback = None, receive_callback = None):
        print("MQTT initiated..")
        super(MQTTCommunicationProtocol, self).__init__(config, send_callback, receive_callback)
        self.brokers = self.config["bootstrap_servers"]
        self.topic = self.config["topic"]
        self.time_interval = self.config["time_interval"]
        #self.packet["id"] = self.config["device_id"]

    def _send_to_single_broker(self, broker, data):

        # Define on_publish event function
        def on_publish(client, userdata, mid):
            print("Message Published...mid: {}".format(mid))
            client.disconnect()
            client.loop_stop()

        def on_connect(client, userdata, flags, rc):
            print("on_connect:", end=': ')
            if rc==0:
                client.connected_flag=True #set flag
                print("connected OK")
            else:
                print("Bad connection Returned code=", rc)
                client.bad_connection_flag=True

        def on_subscribe(client, obj, mid, granted_qos):
            print("Subscribed: " + str(mid) + " " + str(granted_qos))

        def on_message(client, userdata, msg):
            print("on_message:", end=': ')
            print(msg)
            print("on message callback called...\n")

        # Connect with MQTT Broker
        try:
            # Initiate MQTT Client
            mqttc = mqtt.Client()
            print("Authorization:", end=': ')
            print(mqttc.username_pw_set(broker['user'], broker['password']))

            # Register callback function
            mqttc.on_publish = on_publish
            mqttc.on_connect = on_connect
            mqttc.on_message = on_message
            try:
                mqttc.loop_start()
                print("connecting", end=': ')
                print(mqttc.connect(broker['ip_address'], broker['port'])) #connect to broker

                print("subscribing:", end=': ')
                print(mqttc.subscribe(self.topic), qos=1)
            except:
                print("connection to {}:{} failed".format(broker['ip_address'], broker['port']))
                raise Exception("not connected")

            print(data)
            msg = {}
            msg["timestamp"] = data["msg"]["timestamp"] * 1000
            msg["sensor_id"] = data["msg"]["custom_id"]
            msg["value"] = data["msg"]["values"]
            print(msg)
            print("publishing:", end=': ')
            print(mqttc.publish(self.topic, json.dumps(msg), qos=1))

        except Exception as e:
            print(e)
            print("something went wrong while sending message")

    def send(self, data, callback = None):
        if not callback:
            callback = self.send_callback

        for broker in self.brokers:
            self._send_to_single_broker(broker, data)

        if callback:
            callback()

    def receive(self, callback = None):
        pass
