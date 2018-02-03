from .device import Device
import copy

class KY_35(Device):

	values = [
		{
		"name": "magnetic_field",
		"value": None,
		"unit":"mV"
		}
	]

	def __init__(self, config, callback):
		super(KY_35, self).__init__(config, callback)
		self.init_input_outputs(self.__decide_io)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		values = copy.deepcopy(self.values)
		values[0]["value"] = self.input_outputs["Analog"].get_state()
		return values

	def __decide_io(self, io_name):
		if io_name == "Analog" and self.board == "raspberry_pi":
			from input_output import GPIOADCInput
			return GPIOADCInput
