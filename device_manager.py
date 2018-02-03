from threading import Thread
import logging
from device_enum import DeviceEnum, device_constructors

class DeviceManager:

	devices = {}
	devices_config = {}
	callback = None
	board = None

	def __init__(self, devices_config, board, callback):
		self.devices_config = devices_config
		self.callback = callback
		self.board = board
		self.init_devices()

	def init_devices(self):
		for device_config in self.devices_config:
			self.init_device(device_config)

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


