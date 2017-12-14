import threading
import logging
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
		if not callback:
			callback = self.send_callback
		for protocol_id in self.communication_protocols:
			self.communication_protocols[protocol_id].send(data, callback) 

