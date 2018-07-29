import os
from random import randint
import threading
import logging
import time
from tinydb import TinyDB
from security_communication.secure_communication_enum import SecurityEnum, CommunicationEnum, security_constructors, communication_constructors

class CommunicationManager:

	communication_protocols = {}
	communication_protocols_config = {}
	send_callback = None
	receive_callback = None

	def __init__(self, communication_protocols_config, send_callback, receive_callback):
		self.communication_protocols_config = communication_protocols_config
		self.send_callback = send_callback
		self.receive_callback = receive_callback
		self.init_communication_protocols()

	def init_communication_protocols(self):
		for communication_protocol_config in self.communication_protocols_config:
			self.init_communication_protocol(communication_protocol_config)

	def init_communication_protocol(self, communication_protocol_config):
		communication_type = CommunicationEnum[communication_protocol_config["communication_type"]].value
		communication_protocol = communication_constructors[communication_type](communication_protocol_config, self.send_callback, self.receive_callback)
		security_type = SecurityEnum[communication_protocol_config["security_type"]].value
		self.communication_protocols[communication_protocol_config["id"]] = security_constructors[security_type](communication_protocol_config, communication_protocol, self.send_callback, self.receive_callback)

	def send_all(self, data, callback = None):
		self.save_to_local_storage(data)
		if not callback:
			callback = self.send_callback
		for protocol_id in self.communication_protocols:
			self.communication_protocols[protocol_id].send(data, callback)

	def save_to_local_storage(self, data):
		failed = True
		attempt = 0
		while failed and attempt < 5:
			try:
				db = TinyDB(data["msg"]["custom_id"] + '_db.json')
				db.insert(data["msg"])
				failed = False
			except Exception as e:
				os.rename(data["msg"]["custom_id"] + '_db.json', data["msg"]["custom_id"] + '_db_fault' +str(time.time())+ '.json')
				attempt = attempt + 1
				time.sleep(randint(1, 3))

		if failed and attempt >= 5:
			print('Data could not be saved locally')
