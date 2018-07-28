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
			geturl = "http://iot.pcxd.me:3000/api/consumers/consume/1/_search"
			getheaders = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MzI3ODYyMzIsImlzcyI6ImlvdHBsYXRmb3JtIiwic3ViIjoiMSJ9.kvPImDLeEEzQj7S2IiIDa_DO1lxMObnPVftyHWRhcmbwhoYj4Rk6s8mE37GZusU5yVKCq00BC9rq57wDNTuWWfToRLo0FpEKJ3Eqp52Vhnea27RQl-PoMZlom9BdBR-ld2TTlDIIUnQ06lUXtaP174Hxr-mvMn_Gr_dzHU3u6kMxVtpnZhrYH38ZqZ1CLzAutu3dZ-DnzL3QQS7JB5f5L2qaxI2jVWxYLxVwU7O2-BGrawbmjc4gLoCobb8y6GkkgE9JxcPYQJ20SFAZwhibwlwtDJIctNpNyVNFFRw39KUEFZosX00nVzEH4DtgVlrom6fCRolO2BXkPuRxemHsUVj_8xK8U9XEdYwmls2F8R3i2-joB4CoOO0Z0WkDljnOlf6IbiX9cmSbOU7nKMIEcOQLSg0Z-gpul-VynAzXl6HqXjr9-2fHpTDX6U5xr9hHBFkk8nLLnrVaEZ1lDxd97nD5wBIjFRgMtDW2F85enzD3cUndR_ZwQGlKe9QQ4SHi1y0wE5MzKfJhJtvRxMOFqiKt2LtdSOPPWFH55f_h1t4Z49evBqa5TdcQ9yusc7DnkboYwqmT6MnMrHVLzV18zb-bomR6XW_3t8Z9WBIX6B4c6ey1FHOeV0HypQEs6VlW3A9UM_LwycluX2wpQAZiEaDeNip0LX1RNt62H2owSu8"}
			print(requests.get(geturl, headers=getheaders))
			
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
