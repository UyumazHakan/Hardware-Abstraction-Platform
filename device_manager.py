from threading import Thread
import logging
from device_enum import DeviceEnum, device_constructors
import time

class DeviceManager:

	devices = {}
	devices_config = {}
	callback = None
	board = None
	connected = 0

	def __init__(self, devices_config, board, callback):
		self.devices_config = devices_config
		self.callback = callback
		self.board = board
		self.init_devices()

	def init_devices(self):
		for device_config in self.devices_config:
			try:
				self.init_device(device_config)
				self.connected = self.connected + 1
			except:
				print("could not connect to sensor : {} , id: {}".format(device_config["type"], device_config["custom_id"]))

	def init_device(self, device_config):
		device_type = DeviceEnum[device_config["type"]].value
		device_config["board_type"] = self.board
		self.devices[device_config["id"]] = device_constructors[device_type](device_config, self.callback)

	def read_all(self):
		for device in self.devices.values():
			if not device.is_switch:
				device_thread = Thread(target=device.read_value_loop,  kwargs={'callback': self.callback})
				device_thread.daemon = True
				device_thread.start()
				time.sleep(1)
