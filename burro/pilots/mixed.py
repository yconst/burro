'''

mixed.py

Mixed pilots using CNNs combined with manual control.

'''

import os
import math
import random
from operator import itemgetter
from datetime import datetime

import methods

from rc import RC
from f710 import F710
from pilots import BasePilot
from cnn import KerasCategorical

from pilot import BasePilot


class MixedRC(BasePilot):
    '''
    A pilot that combines a CNN with RC throttle control.
    '''

    def __init__(self, keras_pilot, rcpilot, **kwargs):
        self.RCPilot = rcpilot
        self.KerasCategoricalPilot = keras_pilot
        super(MixedRC, self).__init__(**kwargs)

    def decide(self, img_arr):
        rc_angle, rc_throttle = self.RCPilot.decide(img_arr)
        keras_angle, keras_throttle = self.KerasCategoricalPilot.decide(
            img_arr)
        return keras_angle, rc_throttle

    def pname(self):
        return self.KerasCategoricalPilot.pname() + " + RC"


class MixedF710(BasePilot):
    '''
    A pilot that combines a CNN with Gamepad throttle control.
    '''

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
        return self.KerasCategoricalPilot.pname() + " + F710 Gamepad"
