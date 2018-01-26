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
		if self.board == "raspberry_pi":
			from input_output import GPIODHTInput
			self.dht = GPIODHTInput(config["input_output"]["0"])
		self.read_value_imp = self.__read_value

	def __read_value(self):
		humidity, temperature = self.dht.get_state()
		values = copy.deepcopy(self.values)
		values[0]["value"] = temperature
		values[1]["value"] = humidity
		return values
		 
 



