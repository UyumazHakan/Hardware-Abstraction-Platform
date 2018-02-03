from device.device import Device
import time
import copy

class KY_36(Device):

	values = [
		{
		"name": "metal_touch",
		"value": None,
		"unit":"mV"
		},
		{
		"name": "is_touched",
		"value": None,
		"unit": "boolean"
		}
	]

	def __init__(self, config, callback):
		super(KY_36, self).__init__(config, callback)
		self.init_input_outputs(self.__decide_io)
		self.is_switch = True
		self.input_outputs["Digital"].on_change(self.__on_trigger)
		self.read_value_imp = self.__read_value

	def __on_trigger(self, channel):
		self.read_value(self.callback)

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
