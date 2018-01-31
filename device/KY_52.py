from device.device import Device
import time
import copy

class KY_52(Device):

	values = [
		{
		"name": "temperature",
		"value": None,
		"unit":"celcius"
		},
		{
		"name": "pressure",
		"value": None,
		"unit": "pascal"
		},
                {
		"name": "altitude",
		"value": None,
		"unit": "meter"
		},
                {
		"name": "sealevel_pressure",
		"value": None,
		"unit": "pascal"
		}
	]

	def __init__(self, config, callback):
		super(KY_52, self).__init__(config, callback)
		if self.board == "raspberry_pi":
			from input_output import GPIOBMP280Input
			self.bmp280 = GPIOBMP280Input(config["input_output"]["0"])
			self.input_outputs.append(self.bmp280)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		t,p,a,s = self.bmp280.get_state()
		values = copy.deepcopy(self.values)
		values[0]["value"] = t
		values[1]["value"] = p
		values[2]["value"] = a
		values[3]["value"] = s
		return values
		 
 



