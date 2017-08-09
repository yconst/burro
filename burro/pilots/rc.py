'''

rc.py

Pilots using RC control

'''

import os
import math
import random
import time
from operator import itemgetter
from datetime import datetime
from pilots import BasePilot

from navio import rcinput

import methods
from config import config


class RC(BasePilot):
    '''
    A pilot for NAVIO2 RC input
    '''
    def __init__(self, **kwargs):
        self.rcin = rcinput.RCInput()
        self.throttle_center = 1500
        self.yaw_center = 1500
        self.calibrated = False
        super(RC, self).__init__(**kwargs)

    def decide(self, img_arr):
        if float(self.rcin.read(config.rc.arm_channel)) > 1490:
            if not self.calibrated:
                self.calibrate_rc(self.rcin)

            rc_pos_throttle = float(self.rcin.read(config.rc.throttle_channel))
            rc_pos_yaw = float(self.rcin.read(config.rc.yaw_channel))

            throttle = (rc_pos_throttle - self.throttle_center) / 500.0
            yaw = (rc_pos_yaw - self.yaw_center) / 500.0
        else:
            throttle = 0
            yaw = 0
            self.calibrated = False

        return methods.yaw_to_angle(yaw), throttle

    def calibrate_rc(self, rcin):
        print("Please center your receiver sticks")
        time.sleep(2.00)

        print("Calibrating RC Input...")
        yaw = 0
        throttle = 0

        for x in range(0, 100):
            yaw += float(rcin.read(config.rc.yaw_channel))
            throttle += float(rcin.read(config.rc.throttle_channel))

            time.sleep(0.02)

        yaw /= 100.0
        throttle /= 100.0

        self.throttle_center = throttle
        self.yaw_center = yaw

        self.calibrated = True

        print("Done")

    def pname(self):
        return "RC"
