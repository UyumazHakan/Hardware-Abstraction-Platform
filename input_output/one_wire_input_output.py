import glob
import time
from input_output.input_output import InputOutput
from .gpio_input import GPIOInput


class OneWireInputOutput(InputOutput):
	def __init__(self, config):
		super(OneWireInputOutput, self).__init__(config)
		self.input_gpio = GPIOInput({"pin": config["pin"], "gpiopullupdown": "up"})
		while True:
			try:
				device_folder = glob.glob(config["base_dir"]+"28*")[0]
				break
			except IndexError:
				time.sleep(0.5)
				continue
		self.device_file = device_folder + "/" + config["slave_name"]

	def get_state(self):
		f = open(self.device_file, 'r')
		lines = f.readlines()
		f.close()
		return lines



