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
        super(MQTTCommunicationProtocol, self).__init__(config, send_callback, receive_callback)
        self.brokers = self.config["bootstrap_servers"]
        self.topic = self.config["topic"]
        self.time_interval = self.config["time_interval"]
        #self.packet["id"] = self.config["device_id"]

    # Define on_publish event function
    def on_publish(self, client, userdata, mid):
        print("Message Published...")

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            client.connected_flag=True #set flag
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)
            client.bad_connection_flag=True

    def on_message(self, client, userdata, msg):
        # print(msg.topic)
        # print(msg.payload)
        # payload = json.loads(msg.payload)
        # print(payload)
        # client.disconnect()
        print("on message callback called...\n")

    def _send_to_single_broker(self, broker, data):
        # Initiate MQTT Client
        mqttc = mqtt.Client()

        # Register publish callback function
        mqttc.on_publish = self.on_publish
        mqttc.on_connect = self.on_connect
        mqttc.on_message = self.on_message

        # Connect with MQTT Broker
        try:
            try:
                mqttc.connect(broker['ip_address'], broker['port']) #connect to broker
                mqttc.username_pw_set(broker['user'], broker['password'])
                mqttc.subscribe(self.topic)
            except:
                print("connection to {}:{} failed".format(broker['ip_address'], broker['broker.port']))
                raise Exception("not connected")

            msg = {}
            msg["timestamp"] = data["msg"]["timestamp"] * 1000
            msg["sensor_id"] = data["msg"]["custom_id"]
            msg["value"] = data["msg"]["values"]

            print(json.dumps(msg))
            mqttc.publish(self.topic, json.dumps(msg))
            #Loop forever
            mqttc.loop_forever()
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
