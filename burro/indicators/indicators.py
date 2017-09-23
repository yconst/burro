
import methods
from config import config

class Indicator(object):
	'''
	Generic class for onboard state indicators, such as
	LEDs
	'''

	def set_state(self, state):
		'''
		Set the state of the indicator. Common values are:
		warmup, ready, standby, recording, error
		'''
		pass


class NAVIO2LED(Indicator):
	'''
	Abstraction of the NAVIO2 LED indicator
	'''

	def __init__(self, **kwargs):
		from navio2 import leds
		self.led = leds.Led()
		super(NAVIO2LED, self).__init__(**kwargs)

	def set_state(self, state):
		if state == "warmup":
			self.led.setColor('Yellow')
		elif state == "ready":
			self.led.setColor('Blue')
		elif state == "standby":
			self.led.setColor('Green')
		elif state == "recording":
			self.led.setColor('Red')
		elif state == "error":
			self.led.setColor('Magenta')
