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
        print(msg.topic)
        print(msg.payload)
        payload = json.loads(msg.payload)
        print(payload)
        client.disconnect()

    def _send_to_single_broker(self, broker, data):
        # Initiate MQTT Client
        mqttc = mqtt.Client()

        # Register publish callback function
        mqttc.on_publish = self.on_publish
        mqttc.on_connect = self.on_connect
        mqttc.on_message = self.on_message

        # Connect with MQTT Broker
        try:
            #mqttc.connect(broker.ip_address, broker.port) #connect to broker
            #mqttc.username_pw_set(broker.user, password=broker.password)
            #mqttc.subscribe(self.topic)

            packet = copy.deepcopy(self.packet)
            packet["devices"]["sensors"].append(data["msg"])
            print(json.dumps(packet, indent=4, sort_keys=True))
            #mqttc.publish(self.topic, MQTT_MSG)
            #Loop forever
            #mqttc.loop_forever()
        except:
            print("connection to {}:{} failed".format(broker.ip_address, broker.port))

    def send(self, data, callback = None):
        if not callback:
            callback = self.send_callback

        for broker in self.brokers:
            self._send_to_single_broker(broker, data)

        if callback:
            callback()

    def receive(self, callback = None):
        pass
