import os
import json
import logging
import time
import atexit
from device_manager import DeviceManager
from communication_manager import CommunicationManager
from security_communication.secure_communication_enum import SecurityEnum, CommunicationEnum, security_constructors, communication_constructors

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

	def device_manager_callback(self, data):
		self.communication_manager.send_all(data)

	def communication_manager_send_callback(self):
		print("Successfully sent a packet")

	def communication_manager_receive_callback(self, data):
		pass

	def __init__(self, config_file_directory):
		self.config_file_directory = config_file_directory
		self.update_config()
		if self.config["board_type"] == "raspberry_pi":
			import RPi.GPIO as GPIO
			GPIO.setmode(GPIO.BOARD)
		self.device_manager = DeviceManager(self.config["devices"], self.config["board_type"], self.device_manager_callback)
		self.communication_manager = CommunicationManager(self.config["communication_protocols"], self.communication_manager_send_callback, self.communication_manager_receive_callback)
		time.sleep(5)
		self.device_manager.read_all()



def main():
	with open(config_file_directory) as config_file:
		config = json.loads(config_file.read())
	web_server = security_constructors[SecurityEnum.PlainText.value] \
	({}, \
	communication_constructors[CommunicationEnum.HTTP.value] \
	({"ip": "141.40.254.141", "port": 4000}))
	login_response = web_server.send( \
		{"msg":{"username": config["username"], "password": config["password"]}, \
		"http_header":{"Content-Type": "application/json"}, "http_method": "POST", \
		"http_selector": "/users/authenticate", \
		"http_body_type": web_server.communication_protocol.BodyTypes.RAW})
	token = json.loads(login_response.read().decode("utf-8"))["token"]
	for root, dirs, files in os.walk(config["log_directory"], topdown=False):
		for name in files:
			old_log=os.path.join(root, name)
			response = web_server.send( \
			{"fields":{"id": config["id"]}, \
			"files":{"file":old_log}, \
			"http_header":{"Authorization": "Bearer "+token}, "http_method": "POST", \
			"http_selector": "/devices/upload", \
			"http_body_type": web_server.communication_protocol.BodyTypes.MULTIPART})
			print(response.read())
			status = response.status
			if status == 200:
				os.remove(old_log)
	logging.basicConfig(filename= config["log_directory"] + "log_" + str(int(time.time())) + ".txt", \
		filemode= "w", level=logging.DEBUG, \
		format="%(asctime)s - %(funcName)-25s:%(filename)-30s:%(thread)d - %(levelname)-5s - %(message)s")
	logging.info("Started")
	system_manager = SystemManager(config_file_directory)
	while True:
		pass

def exit_handler():
	with open(config_file_directory) as config_file:
		config = json.loads(config_file.read())
	logging.info("Stopped")
	logging.shutdown()
	if config["board_type"] == "raspberry_pi":
		import RPi.GPIO as GPIO
		GPIO.cleanup()

atexit.register(exit_handler)

if __name__ == "__main__":
	main()