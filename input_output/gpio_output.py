from .gpio_input_output import *
from time import sleep

class GPIOOutput(GPIOInputOutput):
	state = None
	def __init__(self, config):
		super(GPIOOutput, self).__init__(config)
		
		if self.config["initial"] and self.config["initial"] == 0:
			GPIO.setup(self.pin, GPIO.OUT, GPIO.LOW)
			self.state = GPIO.LOW
		elif self.config["initial"] and self.config["initial"] == 1:
			GPIO.setup(self.pin, GPIO.OUT, GPIO.HIGH)
			self.state = GPIO.HIGH
		else:
			GPIO.setup(self.pin, GPIO.OUT)


	def low_output(self):
		GPIO.output(self.pin, GPIO.LOW)
		self.state = GPIO.LOW

	def high_output(self):
		GPIO.output(self.pin, GPIO.HIGH)
		self.state = GPIO.HIGH

   
	def toggle_output(self, time = None):
		GPIO.output(self.pin, not (GPIO.input(self.pin)))
		self.state = not self.state
		if time:
			sleep(time)
			GPIO.output(self.pin, self.state)
			self.state = not self.state

