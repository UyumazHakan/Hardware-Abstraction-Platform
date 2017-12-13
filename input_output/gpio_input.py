from gpio_input_output import *
from time import sleep
from threading import Timer, Thread

class GPIOInput(GPIOInputOutput):
	state = None
	on_change_flag = False
	def __init__(self, config):
		super(GPIOOutput, self).__init__(config)
		self.state = GPIO.input(self.pin)

	def on_change(self, callback):
		def __on_change(callback):
			self.on_change_flag = True
			self.state = GPIO.input(self.pin)
			while self.on_change_flag:
				if self.state is not GPIO.input(self.pin):
					self.state = GPIO.input(self.pin)
					callback_thread = Thread(target=callback, args=(self.state))
					callback_thread.daemon = True
					callback_thread.start()
		on_change_thread = Thread(target=__on_change, args=(callback))
		on_change_thread.daemon = True
		on_change_thread.start()

	def stop_on_change(self):
		self.on_change_flag = False

	def get_state(self):
		self.state = GPIO.input(self.pin)
		return self.state


