import os
import json
dir_path = os.path.dirname(os.path.normpath(os.path.realpath(__file__) + "/.."))
config_file_directory = dir_path+"/config.json"
with open(config_file_directory) as config_file:
	config = json.loads(config_file.read())
if config["board"] == "raspberry_pi":
	from .gpio_input import GPIOInput
	from .gpio_output import GPIOOutput
	from .one_wire_input_output import OneWireInputOutput
elif config["board"] == "odroid":
	from .BME280 import BME280
	from .SI1132 import SI1132