import os
import json
import logging
import time
import atexit
from device_manager import DeviceManager
from communication_manager import CommunicationManager

dir_path = os.path.dirname(os.path.realpath(__file__))
config_file_directory = dir_path+"/config.json"


class SystemManager:

	config_file_directory = None
	config = {}
	device_manager, communication_manager = None, None

	#Updates config according to config file

	def update_config(self):
		logging.info("Config updated")
		with open(self.config_file_directory) as config_file:
			self.config = json.loads(config_file.read())
			logging.debug("New config : " + json.dumps(self.config))

	def device_manager_callback(self):
		pass

	def communication_manager_callback(self):
		pass

	def __init__(self, config_file_directory):
		self.config_file_directory = config_file_directory
		self.update_config()
		self.device_manager = DeviceManager(self.config["devices"], self.device_manager_callback)
		self.communication_manager = CommunicationManager(self.config["communication_protocols"], self.communication_manager_callback)



def main():
	with open(config_file_directory) as config_file:
		config = json.loads(config_file.read())
	logging.basicConfig(filename= config["log_directory"] + "log_" + str(int(time.time())) + ".txt", \
		filemode= "w", level=logging.DEBUG, \
		format="%(asctime)s - %(funcName)-25s:%(filename)-30s:%(thread)d - %(levelname)-5s - %(message)s")
	logging.info("Started")
	system_manager = SystemManager(config_file_directory)

def exit_handler():
	logging.info("Stopped")
	logging.shutdown()

atexit.register(exit_handler)

if __name__ == "__main__":
	main()