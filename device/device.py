class Device:
	input_outputs = []
	callback = None
	config = None
	def __init__(self, config, callback):
		self.callback = callback
		self.config = config

	def __read_value(self):
		pass


	def read_value(self, callback=None):
		value = self.__read_value()
		callback(value) if callback else self.callback(value)

	def read_value_loop(self, interval, callback=None):
		self.read_value(callback)
		t = Timer(interval, read_value_loop, [self, interval, callback])