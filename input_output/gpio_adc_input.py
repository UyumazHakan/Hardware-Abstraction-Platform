from input_output.input_output import InputOutput
from time import sleep
from threading import Timer, Thread
import Adafruit_ADS1x15

class GPIOADCInput(InputOutput):
	def __init__(self, config):
		super(GPIOADCInput, self).__init__(config)
		# assigning the ADS1x15 ADC
		self.ads = self.config["gpioadsvalue"] 
		# choosing the amplifing gain
		self.gain = 1 # +/- 4.096V
		# choosing the sampling rate
		self.sps = 64 # 64 Samples per second
		# assigning the ADC-Channel (1-4)
		self.adc_channel = self.config["gpioadcchannel"]
		# initialise ADC 
		if self.ads == 0x00:
			self.adc = Adafruit_ADS1x15.ADS1015()
		elif self.ads == 0x01:
			self.adc = Adafruit_ADS1x15.ADS1115()

	def get_state(self):
		return self.adc.read_adc(self.adc_channel, self.gain, self.sps)


