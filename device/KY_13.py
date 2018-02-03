from .device import Device
import copy
import math

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
		self.init_input_outputs(self.__decide_io)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		voltage = self.input_outputs["Analog"].get_state()
		temperature = math.log((10000/voltage)*(3300-voltage))
		temperature = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * temperature * temperature)) * temperature)
		temperature = temperature - 273.15
		values = copy.deepcopy(self.values)
		values[0]["value"] = temperature
		return values


	def __decide_io(self, io_name):
		if io_name == "Analog" and self.board == "raspberry_pi":
			from input_output import GPIOADCInput
			return GPIOADCInput
			