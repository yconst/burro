#-*- coding:utf-8 -*-

'''

rc.py

A pilot using RC control

'''

import time
from pilots import BasePilot

from navio import rcinput, leds, util

import methods
import config

util.check_apm()

class RC(BasePilot):
    '''
    A pilot class using the RC input of the NAVIO2 controller
    '''
    def __init__(self, **kwargs):
        self.rcin = rcinput.RCInput()

        self.led = leds.Led()

        self.throttle_center = config.RC_THROTTLE_CENTER
        self.yaw_center = config.RC_YAW_CENTER
        self.roll_center = config.RC_ROLL_CENTER
        self.calibrated = False

        super(RC, self).__init__(**kwargs)

    def decide(self, img_arr):
        if float(self.rcin.read(4)) > 1490:
            if not self.calibrated:
                self.calibrate_rc(self.rcin)

            self.led.setColor('Green')
            rc_pos_throttle = float(self.rcin.read(config.THROTTLE_CHANNEL))
            rc_pos_yaw = float(self.rcin.read(config.YAW_CHANNEL))

            throttle = (rc_pos_throttle - self.throttle_center) / 500.0
            yaw = (rc_pos_yaw - self.yaw_center) / 500.0
        else:

            self.led.setColor('Blue')
            throttle = 0
            yaw = 0
            self.calibrated = False

        return methods.yaw_to_angle(yaw), throttle

    def calibrate_rc(self, rcin):
        '''
        Accepts a RC controller reference and calibrates
        the RC channels
        '''
        print "Please center your receiver sticks"
        self.led.setColor('Cyan')
        time.sleep(2.00)

        print "Calibrating RC Input..."
        self.led.setColor('Magenta')
        yaw = 0
        throttle = 0
        roll = 0

        for iterator in range(0, 100):
            yaw += float(rcin.read(config.YAW_CHANNEL))
            throttle += float(rcin.read(config.THROTTLE_CHANNEL))
            roll += float(rcin.read(3))

            time.sleep(0.02)

        yaw /= 100.0
        throttle /= 100.0
        roll /= 100.0

        self.throttle_center = throttle
        self.yaw_center = yaw
        self.roll_center = roll

        self.calibrated = True

        print "Done"

    def pname(self):
        return "RC"
        