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
		self.decide_io_imp = self.__decide_io
		super(KY_52, self).__init__(config, callback)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		t,p,a,s = self.input_outputs["Signal"].get_state()
		values = copy.deepcopy(self.values)
		values[0]["value"] = t
		values[1]["value"] = p
		values[2]["value"] = a
		values[3]["value"] = s
		return values
		 
 	def __decide_io(self, io_name):
		if io_name == "Signal" and self.board == "raspberry_pi":
			from input_output import GPIOBMP280Input
			return GPIOBMP280Input



