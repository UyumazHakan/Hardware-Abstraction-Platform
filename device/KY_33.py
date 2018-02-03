from .device import Device
import copy

class KY_33(Device):

	values = [
		{
		"name": "tracking_sensor_modul",
		"value": None,
		"unit":"boolean"
		}
	]

	def __init__(self, config, callback):
		super(KY_33, self).__init__(config, callback)
		self.init_input_outputs(self.__decide_io)
		self.is_switch = True
		self.input_outputs["Signal"].on_change(self.__on_trigger)
		self.read_value_imp = self.__read_value


	def __on_trigger(self, channel):
		self.read_value(self.callback)

	def __read_value(self):
		values = copy.deepcopy(self.values)
		values[0]["value"] = self.input_outputs["Signal"].get_state()
		return values

	def __decide_io(self, io_name):
		if io_name == "Signal" and self.board == "raspberry_pi":
			from input_output import GPIOInput
			return GPIOInput
