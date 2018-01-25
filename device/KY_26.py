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
		super(KY_26, self).__init__(config, callback)
		if self.board == "raspberry_pi":
			from input_output import GPIOADCInput, GPIOInput
			self.digital = GPIOInput(config["input_output"]["0"])
			self.input_outputs.append(self.digital)
			self.analog = GPIOADCInput(config["input_output"]["1"], 0x01, 0)
			self.input_outputs.append(self.analog)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		values = copy.deepcopy(self.values)
		values[0]["value"] = self.analog.get_state()
		values[1]["value"] = self.digital.get_state()
		return values
		 
 


