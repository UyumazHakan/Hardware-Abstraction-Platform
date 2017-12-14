from .device import Device
from input_output import *
from threading import Timer

class KY_01(Device):

	values = [
		{
		"name": "temperature",
		"value": None,
		"unit":"celcius"
		}
	]

	one_wire_input_output = None

	def __init__(self, config, callback):
		super(KY_01, self).__init__(config, callback)
		self.one_wire_input_output = OneWireInputOutput(config[input_output][0])
		self.input_output.append(self.signal_pin)
		self.one_wire_input_output.get_state()
		self.read_value_imp = self.__read_value

	def __read_value(self):
		lines = self.one_wire_input_output.get_state()
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = self.one_wire_input_output.get_state()
			equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			values = self.values
			values[0]["value"] = temp_c
			return values

