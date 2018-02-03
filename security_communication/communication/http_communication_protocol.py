from .communication_protocol import CommunicationProtocol
import json
import copy
import random
import string
import mimetypes
import http.client
from enum import Enum


class HTTPCommunicationProtocol(CommunicationProtocol):
	class BodyTypes(Enum):
		RAW = 1
		MULTIPART = 2

	def __init__(self, config, send_callback = None, receive_callback = None):
		super(HTTPCommunicationProtocol, self).__init__(config, send_callback, receive_callback)
		self.host = self.config["ip"] if self.config["ip"] else self.config["domain"]
		self.port = self.config["port"]
		self.connection = http.client.HTTPConnection (self.host + ":" + str(self.port))
		self.selector = self.config.get("selector", "")




	def send(self, data, callback = None):
		body_type = data.get("http_body_type", self.BodyTypes.RAW)
		if not callback:
			callback = self.send_callback
		selector = self.selector + data.get("http_selector", "")
		if body_type == self.BodyTypes.RAW:
			body = json.dumps(data["msg"])
			header = data["http_header"]
			self.connection.request(data["http_method"], selector, body, header)
		elif body_type == self.BodyTypes.MULTIPART:
			body, header = self.encode_multipart_data(data.get("fields", []), data.get("files", []))
			header.update(data.get("http_header", {}))
			self.connection.request(data["http_method"], selector, body, header)
		if callback:
			callback(self.connection.getresponse())
		return self.connection.getresponse()

	def receive(self, callback = None):
		pass


	def random_string (self, length):
		return ''.join (random.choice(string.ascii_letters) for ii in range(length + 1))

	def encode_multipart_data (self, data, files):
		boundary = self.random_string(30)

		def get_content_type (filename):
			return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

		def encode_field (field_name):
			return ('--' + boundary,
					'Content-Disposition: form-data; name="%s"' % field_name,
					'', str (data [field_name]))

		def encode_file (field_name):
			filename = files [field_name]
			return ('--' + boundary,
					'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
					'Content-Type: %s' % get_content_type(filename),
					'', str(open(filename, 'rb').read ()))

		lines = []
		for name in data:
			lines.extend(encode_field (name))
		for name in files:
			lines.extend(encode_file (name))
		lines.extend(('--%s--' % boundary, ''))
		body = '\r\n'.join(lines)

		headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
				   'content-length': str(len(body))}
		return body, headers
