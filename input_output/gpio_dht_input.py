from input_output.input_output import InputOutput
from time import sleep
from threading import Timer, Thread
import Adafruit_DHT

class GPIODHTInput(InputOutput):
	def __init__(self, config):
		super(GPIODHTInput, self).__init__(config)
		self.pin = self.config["bcm_pin"]
		self.dht = Adafruit_DHT.DHT11


	def get_state(self):
		return Adafruit_DHT.read_retry(self.dht, self.pin)


