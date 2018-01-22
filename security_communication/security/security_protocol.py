from security_communication.secure_communication_protocol import SecureCommunicationProtocol



class SecurityProtocol(SecureCommunicationProtocol):

	communication_protocol = None

	def __init__(self, config, communication_protocol, send_callback = None, receive_callback = None):
		super(SecurityProtocol, self).__init__(config, send_callback, receive_callback)
		self.communication_protocol = communication_protocol

	def send(self, data, callback = None):
		pass

	def receive(self, data, callback = None):
		pass