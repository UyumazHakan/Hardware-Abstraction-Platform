from .communication_protocol import CommunicationProtocol
import json
import copy
import random
import string
import mimetypes
import http.client
from enum import Enum
import requests
import time



class HTTPCommunicationProtocol(CommunicationProtocol):

	def __init__(self, config, send_callback = None, receive_callback = None):
		super(HTTPCommunicationProtocol, self).__init__(config, send_callback, receive_callback)
		self.servers = self.config["bootstrap_servers"]
		self.topic = self.config["topic"]
		self.time_interval = self.config["time_interval"]

	def _send_to_single_server(self, server, data):

		headers = {"Authorization":"Bearer "+server['password'], 'content-type': 'application/json'}
		msg = {}
		msg["timestamp"] = data["msg"]["timestamp"] * 1000
		msg["sensor_id"] = data["msg"]["custom_id"]
		msg["value"] = data["msg"]["values"]
		url = "http://" +server['ip_address']+":"+ str(server['port'])

		failed = True
		attempt = 0

		while failed and attempt < 5:
			try:
				response = requests.post(url, data=json.dumps(msg), headers=headers)
				if response.status_code == 200:
					failed = False
				else:
					raise Exception("request failed")

			except Exception as e:
				print(e)
				print("HTTP: something went wrong while sending message")
				attempt = attempt + 1

			time.sleep(5)

		if failed and attempt > 4:
			print("server denied to save data 5 times consecutively. Data is probably saved locally")


	def send(self, data, callback = None):
		if not callback:
		    callback = self.send_callback

		for server in self.servers:
			self._send_to_single_server(server, data)

		if callback:
		    callback()

	def receive(self, callback = None):
		pass
