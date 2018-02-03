from input_output import SI1132
from input_output import BME280
from device.device import Device
import copy



class WEATHER2_BOARD(Device):

	values = [
		{
		"name": "UV_index",
		"value": None,
		"unit": "%%"
		},
		{
		"name": "Visible",
		"value": None,
		"unit": "Lux"
		},
		{
		"name": "IR",
		"value": None,
		"unit":"Lux"
		},
		{
		"name": "temperature",
		"value": None,
		"unit": "'C"
		},
		{
		"name": "humidity",
		"value": None,
		"unit": "%%"
		},
		{
		"name": "pressure",
		"value": None,
		"unit":"hPa"
		},
		{
		"name": "altitude",
		"value": None,
		"unit":"m"
		}
	]

	def __init__(self, config, callback):
		super(WEATHER2_BOARD, self).__init__(config, callback)
		self.si1132 = SI1132(str(config["input_output"][0]["pin"]))
		self.bme280 = BME280(str(config["input_output"][0]["pin"]), 0x03, 0x02, 0x02, 0x02)
		self.read_value_imp = self.__read_value

	def __read_value(self):
		values = copy.deepcopy(self.values)
		values[0]["value"] = self.si1132.readUV() / 100.0
		values[1]["value"] = int(self.si1132.readVisible())
		values[2]["value"] = int(self.si1132.readIR())
		values[3]["value"] = self.bme280.read_temperature()
		values[4]["value"] = self.bme280.read_humidity()
		values[5]["value"] = self.bme280.read_pressure() / 100.0
		values[6]["value"] = self.get_altitude(self.bme280.read_pressure(), 1024.25)
		return values

	def get_altitude(self, pressure, seaLevel):
		atmospheric = pressure / 100.0
		return 44330.0 * (1.0 - pow(atmospheric/seaLevel, 0.1903))

