from input_output import SI1132
from input_output import BME280
from device.device import Device


class WEATHER2_BOARD_PRESSURE(Device):

	def __init__(self, config, callback):
		super(WEATHER2_BOARD_PRESSURE, self).__init__(config, callback)
		self.si1132 = SI1132(str(config["input_output"][0]["pin"]))
		self.bme280 = BME280(str(config["input_output"][0]["pin"]), 0x03, 0x02, 0x02, 0x02)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		value = {
			"name": "pressure",
			"value": None,
			"unit":"hPa"
		}
		value["value"] = self.bme280.read_pressure() / 100.0
		return value
