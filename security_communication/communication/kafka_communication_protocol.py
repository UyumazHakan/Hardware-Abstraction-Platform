from .communication_protocol import CommunicationProtocol
from threading import Timer, Lock


class KafkaCommunicationProtocol(CommunicationProtocol):

	producer = None
	topic = None
	send_buffer = []
	time_interval = 1
	send_lock = Lock()

	def __init__(self, config, send_callback = None, receive_callback = None):
		super(KafkaCommunicationProtocol, self).__init__(config, send_callback, receive_callback)
		target = self.config["ip"] + ":" + self.config.get("port", "9092")
		self.producer = KafkaProducer(bootstrap_servers=[target])
		self.topic = self.config["topic"]
		self.time_interval = self.config["time_interval"]
		send_timer = Timer(self.time_interval, self.__send_buffer, [self])
		send_timer.start()


	def __send_buffer(self):
		self.send_lock.acquire()
		for (data, callback) in self.send_buffer:
			topic = topic + data.get("sub_topic", "")
			self.producer.send(topic, data["msg"])
			if callback:
				callback()
		self.send_buffer = []
		self.send_lock.release()
		send_timer = Timer(self.time_interval, self.__send_buffer, [self])
		send_timer.start()


	def send(self, data, callback = None):
		self.send_lock.acquire()
		if not callback:
			callback = self.send_callback
		self.send_buffer.append((data, callback))
		self.send_lock.release()

	def receive(self, callback = None):
		pass


