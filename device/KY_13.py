from .device import Device
import copy

class KY_13(Device):

	values = [
		{
		"name": "temperature",
		"value": None,
		"unit":"celcius"
		}
	]

	def __init__(self, config, callback):
		super(KY_13, self).__init__(config, callback)
		if self.board == "raspberry_pi":
			from input_output import GPIOADCInput
			self.analog = GPIOADCInput(config["input_output"]["1"], 0x01, 0)
			self.input_outputs.append(self.analog)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		values = copy.deepcopy(self.values)
		values[0]["value"] = self.analog.get_state()
		return values
