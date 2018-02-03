from .communication_protocol import CommunicationProtocol
from threading import Timer, Lock
from kafka import KafkaProducer
import json
import copy

class KafkaCommunicationProtocol(CommunicationProtocol):

	producer = None
	topic = None
	send_buffer = []
	time_interval = 1
	send_lock = Lock()
	packet = {
		"id": None,
		"devices": {
			"sensors": []
		}

	}

	def __init__(self, config, send_callback = None, receive_callback = None):
		super(KafkaCommunicationProtocol, self).__init__(config, send_callback, receive_callback)
		self.bootstrap_servers = list(map(lambda x: str(x["ip_address"]) + ":" + str(x["port"]), self.config["bootstrap_servers"]))
		self.producer = KafkaProducer(
			bootstrap_servers=self.bootstrap_servers, \
			value_serializer=lambda v: json.dumps(v).encode('utf-8'), \
			api_version=(0,self.config["api_version"]), \
			compression_type="gzip")
		self.topic = self.config["topic"]
		self.time_interval = self.config["time_interval"]
		self.packet["id"] = self.config["device_id"]
		send_timer = Timer(self.time_interval, self.__send_buffer, [])
		#send_timer.start()


	def __send_buffer(self):
		print("Sending...")
		self.send_lock.acquire()
		print(self.send_buffer)
		packets = {}
		for (data, callback) in self.send_buffer:
			topic = self.topic + data.get("sub_topic", "")
			if not topic in packets:
				packets[topic] = self.packet
			packets[topic]["devices"]["sensors"].append(data["msg"])
		for topic in packets:
			self.producer.send(topic, packets[topic])
			print("Sent:", packets[topic])
			if callback:
				callback()
		self.send_buffer = []
		self.send_lock.release()
		send_timer = Timer(self.time_interval, self.__send_buffer, [])
		send_timer.start()


	def send(self, data, callback = None):
		#self.send_lock.acquire()
		if not callback:
			callback = self.send_callback
		topic = self.topic + data.get("sub_topic", "")
		packet = copy.deepcopy(self.packet)
		packet["devices"]["sensors"].append(data["msg"])
		self.producer.send(topic, packet)
		print(json.dumps(packet, indent=4, sort_keys=True))
		if callback:
			callback()
		#self.send_buffer.append((data, callback))
		#self.send_lock.release()

	def receive(self, callback = None):
		pass


