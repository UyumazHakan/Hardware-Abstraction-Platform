from .device import Device
from threading import Timer
import copy

class KY_01(Device):

	values = [
		{
		"name": "temperature",
		"value": None,
		"unit":"celcius"
		}
	]

	def __init__(self, config, callback):
		super(KY_01, self).__init__(config, callback)
		self.init_input_outputs(self.__decide_io)
		self.input_outputs["Signal"].get_state()
		self.read_value_imp = self.__read_value

	def __read_value(self):
		lines = self.input_outputs["Signal"].get_state()
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = self.input_outputs["Signal"].get_state()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			values = copy.deepcopy(self.values)
			values[0]["value"] = temp_c
			return values

	def __decide_io(self, io_name):
		if io_name == "Signal" and self.board == "raspberry_pi":
			from input_output import OneWireInputOutput
			return OneWireInputOutput

