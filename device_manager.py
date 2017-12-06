import threading
import logging
from device_enum import DeviceEnum, device_constructors

class DeviceManager:

	devices = {}
	devices_config = {}

	def __init__(self, devices_config, callback):
		self.devices_config = devices_config
		self.init_devices()

	def init_devices(self):
		for device_config in self.devices_config:
			self.init_device(device_config)

	def init_device(self, device_config):
		device_type = DeviceEnum[device_config["type"]]
		devices[device_config["id"]] = device_constructors[device_type](device_config, self.callback)

	def callback(self):
		pass
