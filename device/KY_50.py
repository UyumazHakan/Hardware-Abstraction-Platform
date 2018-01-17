from device.device import Device
import time
import copy

class KY_50(Device):

	values = [
		{
		"name": "time_elapsed",
		"value": None,
		"unit":"ms"
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
		if self.board is "raspberry_pi":
			from input_output import GPIOOutput, GPIOInput
			self.trigger = GPIOOutput(config["input_output"]["0"])
			self.input_outputs.append(self.trigger)
			self.echo = GPIOInput(config["input_output"]["1"])
			self.input_outputs.append(self.echo)
			self.trigger.low_output()
		self.read_value_imp = self.__read_value

	def __read_value(self):
		self.trigger.toggle_output(0.00001)
		fail_time = time.time()
		start_time = time.time()
		while self.echo.get_state() == 0:
			start_time = time.time()
			if start_time - fail_time > 0.5:
				return self.__read_value()
		stop_time = time.time()
		while self.echo.get_state() == 1:
			stop_time = time.time()
		time_difference = stop_time - start_time
		distance = (time_difference * 34300) / 2
		values = copy.deepcopy(self.values)
		values[0]["value"] = time_difference * 1000
		values[1]["value"] = distance
		return values
		 
 


