"""
drive.py

Starts a driving loop

Usage:
    drive.py [--pilot=<name>] [--model=<name>]

Options:
  --pilot=<name>   pilot name, one of rc, nn [default: rc]
  --model=<name>   model name if pilot is nn [default: models/default.h5]
"""

import sys
import time
from navio import rcinput, pwm, leds, util, mpu9250

from docopt import docopt

import config
from pilots import KerasCategorical
from pilots import RC

util.check_apm()

class Rover(object):

    def __init__(self):
        self.drift_gain = 0.15
        arguments = docopt(__doc__)
        self.set_pilot(arguments['--pilot'], arguments['--model'])

    def run(self):
        self.led = leds.Led()
        self.led.setColor('Yellow')

        self.th_pwm = pwm.PWM(2)
        self.th_pwm.set_period(50)

        self.st_pwm = pwm.PWM(0)
        self.st_pwm.set_period(50)

        self.imu = mpu9250.MPU9250()

        if self.imu.testConnection():
            print "IMU Connection established"
        else:
            sys.exit("IMU Connection failed")

        self.imu.initialize()

        time.sleep(1)

        while True:
            
            pilot_yaw, pilot_throttle = self.pilot.decide()

            m9a, m9g, m9m = self.imu.getMotion9()
            drift = m9g[2]

            th = min(1, max(-1, -pilot_throttle))
            st = min(1, max(-1, -pilot_yaw - drift * self.drift_gain))

            self.set_throttle(value=th, pwm_in=self.th_pwm)
            self.set_throttle(value=st, pwm_in=self.st_pwm)

            time.sleep(0.02)

    def set_throttle(self, value, pwm_in):
        pwm_val = 1.5 + value * 0.5
        pwm_in.set_duty_cycle(pwm_val)

    def set_pilot(self, pilot, model_path):
        if pilot == 'rc':
            self.pilot = RC()
        else:
            self.pilot = KerasCategorical(model_path)

if __name__ == "__main__":
    rover = Rover()
    rover.run()


