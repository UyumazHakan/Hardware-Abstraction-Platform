from ..secure_communication_protocol import SecureCommunicationProtocol

class CommunicationProtocol(SecureCommunicationProtocol):

	def __init__(self, config, send_callback = None, receive_callback = None):
		super(CommunicationProtocol, self).__init__(config, send_callback, receive_callback)

	def send(self, data, callback = None):
		pass

	def receive(self, data, callback = None):
		pass