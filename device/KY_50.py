from device.device import Device
from input_output import GPIOOutput, GPIOInput
from threading import Timer
import time

class KY_50(Device):

	values = [
		{
		"name": "time_elapsed",
		"value": None,
		"unit":"sec"
		},
		{
		"name": "distance",
		"value": None,
		"unit": "cm"
		}
	]
	trigger = None
	echo = None

	def __init__(self, config, callback):
		super(KY_50, self).__init__(config, callback)
		self.trigger = GPIOOutput(config["input_output"]["0"])
		self.input_outputs.append(self.trigger)
		self.echo = GPIOInput(config["input_output"]["1"])
		self.input_outputs.append(self.echo)
		self.trigger.low_output()
		self.read_value_imp = self.__read_value

	def __read_value(self):
		self.trigger.toggle_output(0.00001)
		start_time = time.time()
		while self.echo == 0:
			start_time = time.time()
		stop_time = time.time()
		while self.echo == 1:
			stop_time = time.time()
		time_difference = stop_time - start_time
		distance = (time_difference * 34300) / 2
		values = self.values
		values[0]["value"] = time_difference
		values[1]["value"] = distance
		return values
		 
 


