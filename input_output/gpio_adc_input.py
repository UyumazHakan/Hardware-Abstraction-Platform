from input_output.input_output import InputOutput
from time import sleep
from threading import Timer, Thread
from Adafruit_ADS1x15 import ADS1x15

class GPIOADCInput(InputOutput):
	def __init__(self, config, ads, channel):
		super(GPIOADCInput, self).__init__(config)
		# assigning the ADS1x15 ADC
		self.ads = ads 
		# choosing the amplifing gain
		self.gain = 4096  # +/- 4.096V
		# choosing the sampling rate
		self.sps = 64   # 64 Samples per second
		# assigning the ADC-Channel (1-4)
		self.adc_channel = channel
		# initialise ADC (ADS1115)
		self.adc = ADS1x15(ic=ads)

	def get_state(self):
		return self.adc.readADCSingleEnded(self.adc_channel, self.gain, self.sps)


