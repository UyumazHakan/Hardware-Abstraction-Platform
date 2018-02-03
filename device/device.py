from threading import Timer
import time

class Device:

	def __init__(self, config, callback):
		self.is_switch = False
		self.input_outputs = {}
		self.callback = callback
		self.config = config
		self.board = self.config["board_type"]


	def read_value(self, callback=None):
		values = self.read_value_imp()
		data = {"sub_topic":"","msg":{"id": self.config["id"], "timestamp":int(time.time()), "values": values}}
		callback(data) if callback else self.callback(data)

	def read_value_loop(self, interval = None, callback=None):
		if not interval:
			interval = self.config["interval"]
		self.read_value(callback)
		t = Timer(interval, self.read_value_loop, [interval, callback])
		t.start()

	def init_input_outputs(self, decide_io):
		for io in self.config["input_output"]:
			name = io["name"]
			io_constructor = decide_io(name)
			self.input_outputs[name] = io_constructor(io)
