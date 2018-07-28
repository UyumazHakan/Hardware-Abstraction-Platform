from .communication_protocol import CommunicationProtocol
import json
import copy
import random
import string
import mimetypes
import http.client
from enum import Enum
import requests


class HTTPCommunicationProtocol(CommunicationProtocol):

	def __init__(self, config, send_callback = None, receive_callback = None):
		super(HTTPCommunicationProtocol, self).__init__(config, send_callback, receive_callback)
		self.servers = self.config["bootstrap_servers"]
		self.topic = self.config["topic"]
		self.time_interval = self.config["time_interval"]

	def _send_to_single_server(self, server, data):
		try:
			headers = {"Authorization":"Bearer "+server['password']}
			msg = {}
			msg["timestamp"] = data["msg"]["timestamp"] * 1000
			msg["sensor_id"] = data["msg"]["custom_id"]
			msg["value"] = data["msg"]["values"]
			print(msg)
			url = "http://" +server['ip_address']+":"+ str(server['port'])
			print('sending requests with token.. to ' + url)
			response = requests.post(url, data=json.dumps(msg), headers=headers)
			print("response")
			print(response, end='\n\n')

		except Exception as e:
			print(e)
			print("something went wrong while sending message")


	def send(self, data, callback = None):
		if not callback:
		    callback = self.send_callback

		for server in self.servers:
			self._send_to_single_server(server, data)

		if callback:
		    callback()

	def receive(self, callback = None):
		pass
