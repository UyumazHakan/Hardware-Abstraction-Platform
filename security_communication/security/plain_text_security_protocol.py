from .security_protocol import SecurityProtocol
from ..secure_communication_enum import *


class PlainTextSecurityProtocol(SecurityProtocol):

	def __init__(self, config, communication_protocol, send_callback = None, receive_callback = None):
		super(PlainTextSecurityProtocol, self).__init__(config, communication_protocol, send_callback, receive_callback)


	def send(self, data, callback = None):
		if not callback:
			callback = self.send_callback
		return self.communication_protocol.send(data, callback)

	def receive(self, callback = None):
		if not callback:
			callback = self.receive_callback
		data = self.communication_protocol.receive()
		if callback:
			callback(data)
		return data


