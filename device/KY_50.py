from device import *
from .input_output import *
from threading import Timer
import time

class KY_50(Device):

	trigger = None
	echo = None

	def __init__(self, config, callback):
		super(KY_50, self).__init__(config, callback)
		self.trigger = GPIOOutput(config[input_output][0])
		self.input_output.append(self.trigger)
		self.echo = GPIOInput(config[input_output][0])
		self.input_output.append(self.echo)
		self.echo.low_output()

	def __read_value(self):
		self.trigger.toggle_output(0.00001)
		start_time = time.time()
		while self.echo == 0:
			start_time = time.time()
		while self.echo == 1:
			stop_time = time.time()
		time_difference = stop_time - start_time
		distance = (time_difference * 34300) / 2
		return distance
		 
 


