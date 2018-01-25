from .device import Device
import copy

class KY_31(Device):

	values = [
		{
		"name": "klopf_sensor_modul",
		"value": None,
		"unit":"boolean"
		}
	]
	signal = None

	def __init__(self, config, callback):
		super(KY_31, self).__init__(config, callback)
		self.is_switch = True
		if self.board == "raspberry_pi":
			from input_output import GPIOInput
			self.signal = GPIOInput(config["input_output"]["0"])
			self.input_outputs.append(self.signal)
			self.signal.on_change(self.__on_trigger)
		self.read_value_imp = self.__read_value


	def __on_trigger(self, channel):
		self.read_value(self.callback)

	def __read_value(self):
		values = copy.deepcopy(self.values)
		values[0]["value"] = self.signal.get_state()
		return values
