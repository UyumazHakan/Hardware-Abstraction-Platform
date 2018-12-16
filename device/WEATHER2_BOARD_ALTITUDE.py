from input_output import SI1132
from input_output import BME280
from device.device import Device


class WEATHER2_BOARD_ALTITUDE(Device):

	def __init__(self, config, callback):
		super(WEATHER2_BOARD_ALTITUDE, self).__init__(config, callback)
		self.si1132 = SI1132(str(config["input_output"][0]["pin"]))
		self.bme280 = BME280(str(config["input_output"][0]["pin"]), 0x03, 0x02, 0x02, 0x02)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		return self.get_altitude(self.bme280.read_pressure(), 1024.25)

	def get_altitude(self, pressure, seaLevel):
		atmospheric = pressure / 100.0
		return 44330.0 * (1.0 - pow(atmospheric/seaLevel, 0.1903))
