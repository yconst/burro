"""
drive.py

Starts a driving loop

Usage:
    drive.py [--model=<name>] [--vision=<name>] [--average=<factor>]

Options:
  --model=<name>      model name for nn pilot [default: models/default.h5]
  --vision=<name>     vision sensor type [default: camera]
  --average=<factor>  averaging factor for steering values [default: 0]
"""

from __future__ import division

import sys
import time
from navio import rcinput, pwm, leds, util, mpu9250

from docopt import docopt

import config

from sensors import PiVideoStream

from pilots import KerasCategorical
from pilots import RC
from pilots import Mixed

from remotes import WebRemote

util.check_apm()

class Rover(object):

    def __init__(self):
        self.drift_gain = 0.15
        arguments = docopt(__doc__)
        self.setup_pilots(arguments['--model'])
        self.set_sensors(arguments['--vision'])
        self.set_remote()

        self.avg_factor = float(arguments['--average'])
        self.pilot_yaw = 0
        self.pilot_throttle = 0

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

        time.sleep(0.5)
        self.led.setColor('White')

        self.vision_sensor.start()

        time.sleep(0.5)

        self.led.setColor('Black')

        self.remote.start()

        time.sleep(0.5)

        while True:
            
            pilot_yaw, pilot_throttle = self.pilot.decide(self.vision_sensor.frame)
            
            pilot_yaw = self.avg_factor * self.pilot_yaw + (1.0 - self.avg_factor) * pilot_yaw

            self.pilot_yaw = pilot_yaw
            self.pilot_throttle = pilot_throttle

            m9a, m9g, m9m = self.imu.getMotion9()
            drift = m9g[2]

            th = min(1, max(-1, -pilot_throttle))
            st = min(1, max(-1, -pilot_yaw - drift * self.drift_gain))

            self.set_throttle(value=th, pwm_in=self.th_pwm)
            self.set_throttle(value=st, pwm_in=self.st_pwm)

            time.sleep(0.05)

    def set_throttle(self, value, pwm_in):
        pwm_val = 1.5 + value * 0.5
        pwm_in.set_duty_cycle(pwm_val)

    def setup_pilots(self, model_path):
        #TODO: This should scan for pilot modules and add them
        keras = KerasCategorical(model_path)
        keras.load()
        self.pilots = [
            Mixed(model_path),
            RC(),
            keras
        ]
        self.pilot = self.pilots[0]

    def selected_pilot_index(self):
        return self.pilots.index(self.pilot)

    def set_pilot(self, pilot):
        self.pilot = self.pilots[pilot]

    def list_pilot_names(self):
        return [p.pname() for p in self.pilots]

    def set_sensors(self, vision_sensor):
        if vision_sensor == 'camera':
            self.vision_sensor = PiVideoStream()

    def set_remote(self):
        self.remote = WebRemote(self)

if __name__ == "__main__":
    rover = Rover()
    rover.run()


