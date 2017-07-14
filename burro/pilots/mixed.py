'''

mixed.py

Methods to create, use, save and load pilots. Pilots
contain the highlevel logic used to determine the angle
and throttle of a vehicle. Pilots can include one or more
models to help direct the vehicles motion.

'''
from __future__ import division

import os
import math
import random
from operator import itemgetter
from datetime import datetime

import methods
from rc import RC
from f710 import F710
from pilots import BasePilot, KerasCategorical


class MixedRC(BasePilot):
    def __init__(self, keras_pilot, rcpilot, **kwargs):
        self.RCPilot = rcpilot
        self.KerasCategoricalPilot = keras_pilot
        super(MixedRC, self).__init__(**kwargs)

    def decide(self, img_arr):
        rc_yaw, rc_throttle = self.RCPilot.decide(img_arr)
        keras_angle, keras_throttle = self.KerasCategoricalPilot.decide(
            img_arr)
        return keras_angle, rc_throttle

    def pname(self):
        return self.KerasCategoricalPilot.pname " + RC"


class MixedF710(BasePilot):
    def __init__(self, keras_pilot, f710pilot, **kwargs):
        self.F710Pilot = f710pilot
        self.KerasCategoricalPilot = keras_pilot
        super(MixedF710, self).__init__(**kwargs)

    def decide(self, img_arr):
        f_yaw, f_throttle = self.F710Pilot.decide(img_arr)
        keras_angle, keras_throttle = self.KerasCategoricalPilot.decide(
            img_arr)
        return keras_angle, f_throttle

    def pname(self):
        return self.KerasCategoricalPilot.pname " + F710 Gamepad"
