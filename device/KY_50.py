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

	def __init__(self, config, callback):
		super(KY_50, self).__init__(config, callback)
		self.init_input_outputs(self.__decide_io)
		self.input_outputs["Trigger"].low_output()
		self.read_value_imp = self.__read_value

	def __read_value(self):
		self.input_outputs["Trigger"].toggle_output(0.00001)
		fail_time = time.time()
		start_time = time.time()
		while self.input_outputs["Echo"].get_state() == 0:
			start_time = time.time()
			if start_time - fail_time > 0.5:
				return self.__read_value()
		stop_time = time.time()
		while self.input_outputs["Echo"].get_state() == 1:
			stop_time = time.time()
		time_difference = stop_time - start_time
		distance = (time_difference * 34300) / 2
		values = copy.deepcopy(self.values)
		values[0]["value"] = time_difference * 1000
		values[1]["value"] = distance
		return values

	def __decide_io(self, io_name):
		if io_name == "Echo" and self.board == "raspberry_pi":
			from input_output import GPIOInput
			return GPIOInput
		elif io_name == "Trigger" and self.board == "raspberry_pi":
			from input_output import GPIOOutput
			return GPIOOutput
