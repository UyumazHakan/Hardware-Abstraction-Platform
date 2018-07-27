from .security_protocol import SecurityProtocol
from ..secure_communication_enum import *

from Crypto import Random
from Crypto.PublicKey import RSA
import base64

# Asymmetric Crypto Protocol
class AsymmetricSecurityProtocol(SecureCommunicationProtocol):

	communication_protocol = None

	def __init__(self, config, communication_protocol, send_callback = None, receive_callback = None):
		super(AsymmetricSecurityProtocol, self).__init__(config, communication_protocol, send_callback, receive_callback)

	def send(self, data, callback = None):
		if not callback:
			callback = self.send_callback
		
		pub_key = self.read_public_key(pub_key_file)
		
		return self.communication_protocol.send(self.encrypt_message(data, pub_key), callback)

	def receive(self, callback = None):
		if not callback:
			callback = self.receive_callback
		data = self.communication_protocol.receive()
		if callback:
			callback(data)
		return data

	def read_publickey(pub_key_file):
		f = open(pub_key_file,'r')
		key = RSA.importKey(f.read(), passphrase=None)
		return key

	def encrypt_message(a_message , publickey):
		encrypted_msg = publickey.encrypt(a_message, 32)[0]
		encoded_encrypted_msg = base64.b64encode(encrypted_msg) # base64 encoded strings are database friendly
		return encoded_encrypted_msg