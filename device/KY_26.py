from device.device import Device
import time
import copy

class KY_26(Device):

	values = [
		{
		"name": "voltage",
		"value": None,
		"unit":"mV"
		},
		{
		"name": "extreme_value",
		"value": None,
		"unit": "boolean"
		}
	]

	def __init__(self, config, callback):
		self.decide_io_imp = self.__decide_io
		super(KY_25, self).__init__(config, callback)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		values = copy.deepcopy(self.values)
		values[0]["value"] = self.input_outputs["Analog"].get_state()
		values[1]["value"] = self.input_outputs["Digital"].get_state()
		return values

	def __decide_io(self, io_name):
		if io_name == "Digital" and self.board == "raspberry_pi":
			from input_output import GPIOInput
			return GPIOInput
		elif io_name =="Analog" and self.board == "raspberry_pi":
			from input_output import GPIOADCInput
			return GPIOADCInput
