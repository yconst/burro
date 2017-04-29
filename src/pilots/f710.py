'''

f710.py

A pilot using the F710 gamepad

'''

import os
import math
import random
import time

from operator import itemgetter
from datetime import datetime
from pilots import BasePilot

from navio import leds

from inputs import get_gamepad

import config

class F710(BasePilot):
    def __init__(self, **kwargs):
        self.led = leds.Led()
        super(F710, self).__init__(**kwargs)
        self.throttle = 0.0
        self.yaw = 0.0

    def decide(self, img_arr):

        self.led.setColor('Green')

        events = get_gamepad()

        for event in events:
            print(event.ev_type, event.code, event.state)
            if (event.code == 'ABS_Z'):
                self.yaw = (float(event.state) - 128) / 128.0
            elif (event.code == 'ABS_HAT0Y'):
                self.throttle = float(event.state)

        return self.yaw, self.throttle

    def pname(self):
        return "F310/F710 Gamepad"

