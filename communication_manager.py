import threading
import logging
from secure_communication_enum import SecurityEnum, CommunicationEnum, security_constructors

class CommunicationManager:

	communication_protocols = {}
	communication_protocols_config = {}

	def __init__(self, communication_protocols_config, callback):
		self.communication_protocols_config = communication_protocols_config
		self.init_communication_protocols()

	def init_communication_protocols(self):
		for communication_protocol_config in self.communication_protocols_config:
			self.init_communication_protocol(communication_protocol_config)

	def init_communication_protocol(self, communication_protocol_config):
		security_type = SecurityEnum[communication_protocol_config["security_type"]]
		communication_protocols[communication_protocol_config["id"]] = securtiy_constructors[security_type](communication_protocol_config, self.callback)

	def callback(self):
		pass
