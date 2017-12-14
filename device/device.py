from threading import Timer
import time

class Device:
	input_outputs = []
	callback = None
	config = None
	read_value_imp = None

	def __init__(self, config, callback):
		self.callback = callback
		self.config = config


	def read_value(self, callback=None):
		values = self.read_value_imp()
		data = {"sub_topic":"","msg":{"id": self.config["id"], "timestamp":time.time(), "values": values}}
		callback(data) if callback else self.callback(data)

	def read_value_loop(self, interval = None, callback=None):
		if not interval:
			interval = self.config["interval"]
		self.read_value(callback)
		t = Timer(interval, self.read_value_loop, [interval, callback])