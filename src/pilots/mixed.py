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
from pilots import BasePilot, KerasCategorical


class Mixed(BasePilot):
    def __init__(self, model_path, **kwargs):
        self.RCPilot = RC()
        self.KerasCategoricalPilot = KerasCategorical(model_path)
        self.KerasCategoricalPilot.load()
        super(Mixed, self).__init__(**kwargs)

    def decide(self, img_arr):
        rc_yaw, rc_throttle = self.RCPilot.decide(img_arr)
        keras_angle, keras_throttle = self.KerasCategoricalPilot.decide(
            img_arr)
        return keras_angle, rc_throttle

    def pname(self):
        return "Mixed"
