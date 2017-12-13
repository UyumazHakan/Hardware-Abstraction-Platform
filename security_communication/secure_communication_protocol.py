class SecureCommunicationProtocol:
	config = None
	send_callback = None
	receive_callback = None
	def __init__(self, config, send_callback = None, receive_callback = None):
		self.config = config
		self.send_callback = send_callback
		self.receive_callback = receive_callback

	def send(self, data, callback = None):
		pass
		

	def receive(self, callback = None):
		pass