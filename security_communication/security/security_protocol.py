from .secure_communication_protocol import SecureCommunicationProtocol

class SecurtiyProtocol(SecureCommunicationProtocol):

	communication_protocol = None

	def __init__(self, config, send_callback = None, receive_callback = None):
		super(SecurtiyProtocol, self).__init__(config, send_callback, receive_callback)
		communication_type = CommunicationEnum[communication_protocol_config["communication_type"]]
		self.communication_protocol = securtiy_constructors[security_type](self.config, self.callback)

	def send(self, data, callback = None):
		pass

	def receive(self, data, callback = None):
		pass