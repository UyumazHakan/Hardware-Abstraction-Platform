import RPi.GPIO as GPIO
from input_output.input_output import InputOutput

class GPIOInputOutput(InputOutput):
	pin = None
	def __init__(self, config):
		super(GPIOInputOutput, self).__init__(config)
		self.pin = int(config["pin"])
