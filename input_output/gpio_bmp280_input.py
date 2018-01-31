from input_output.input_output import InputOutput
import Adafruit_BMP.BMP280 as BMP280

class GPIOBMP280Input(InputOutput):
	def __init__(self, config):
		super(GPIOBMP280Input, self).__init__(config)
		self.address = self.config["address"]
		self.bmp280 = BMP280.BMP280(address=self.address)


	def get_state(self):
		t = self.bmp280.read_temperature()
		p = self.bmp280.read_pressure()
		a = self.bmp280.read_altitude()
		s = self.bmp280.read_sealevel_pressure()
		return t,p,a,s


