from gpio_input_output import *
from time import sleep

class GPIOOutput(GPIOInputOutput):
	state = None
	def __init__(self, config):
		super(GPIOOutput, self).__init__(config)
		
		if self.config["initial"] and self.config["initial"] == 0:
			GPIO.setup(self.pin, GPIO.IN, GPIO.LOW)
			self.state = GPIO.LOW
		elif self.config["initial"] and self.config["initial"] == 1:
			GPIO.setup(self.pin, GPIO.IN, GPIO.HIGH)
			self.state = GPIO.HIGH
		else:
			GPIO.setup(self.pin, GPIO.IN)


	def low_output(self):
		GPIO.output(self.pin, GPIO.LOW)
		self.state = GPIO.LOW

	def high_output(self):
		GPIO.output(self.pin, GPIO.HIGH)
		self.state = GPIO.HIGH

   
	def toggle_output(self, time = None):
		if not self.state:
			raise Exception("This output pin has no current state.")
		elif self.state == GPIO.LOW:
		 	GPIO.output(self.pin, GPIO.HIGH)
		elif self.state == GPIO.HIGH:
			GPIO.output(self.pin, GPIO.LOW)
		if time:
			sleep(time)
			GPIO.output(self.pin, state)

