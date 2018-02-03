from .gpio_input_output import *
from time import sleep
from threading import Timer, Thread

class GPIOInput(GPIOInputOutput):
	def __init__(self, config):
		super(GPIOInput, self).__init__(config)
		if self.config["gpiopullupdown"] != "none":
			GPIO.setup(self.pin, GPIO.IN, \
				pull_up_down = GPIO.PUD_UP if self.config["gpiopullupdown"] == "up" \
				else GPIO.PUD_DOWN)
		else:
			GPIO.setup(self.pin, GPIO.IN)
		self.state = GPIO.input(self.pin)

	def on_change(self, callback, bouncetime=100):
		GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=callback, bouncetime=bouncetime)

	def stop_on_change(self):
		GPIO.remove_event_detect(self.pin)

	def get_state(self):
		self.state = GPIO.input(self.pin)
		return self.state


