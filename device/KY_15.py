from .device import Device
import copy

class KY_15(Device):

	values = [
		{
		"name": "temperature",
		"value": None,
		"unit":"celcius"
		},
		{
		"name": "humidity",
		"value": None,
		"unit": "percentage"
		}
	]

	def __init__(self, config, callback):
		super(KY_15, self).__init__(config, callback)
		self.init_input_outputs(self.__decide_io)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		humidity, temperature = self.input_outputs["DHT"].get_state()
		values = copy.deepcopy(self.values)
		values[0]["value"] = temperature
		values[1]["value"] = humidity
		return values
		 
 
	def __decide_io(self, io_name):
		if io_name == "DHT" and self.board == "raspberry_pi":
			from input_output import GPIODHTInput
			return GPIODHTInput
