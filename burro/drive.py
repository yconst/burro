"""
drive.py

Starts a driving loop

Usage:
    drive.py [--model=<name>] [--vision=<name>]

Options:
  --model=<name>      model name for nn pilot [default: models/default.h5]
  --vision=<name>     vision sensor type [default: camera]
"""

from __future__ import division

import sys
import time

from docopt import docopt

import methods
import config

from sensors import PiVideoStream

from pilots import (KerasCategorical, 
    RC, F710, MixedRC, MixedF710)

from mixers import AckermannSteeringMixer

from drivers import NAVIO2PWM

from indicators import NAVIO2LED

from remotes import WebRemote

from recorders import FileRecorder

class Rover(object):

    def __init__(self):
        self.f_time = 0
        arguments = docopt(__doc__)
        self.setup_pilots(arguments['--model'])
        self.setup_recorders()
        self.setup_mixers()
        self.set_sensors(arguments['--vision'])
        self.set_remote()

    def run(self):
        self.indicator = NAVIO2LED()
        self.indicator.set_state('warmup')

        time.sleep(0.5)
        self.vision_sensor.start()
        time.sleep(0.5)
        self.remote.start()
        self.indicator.set_state('ready')
        time.sleep(0.5)

        while True:
            start_time = time.time()
            self.step()
            stop_time = time.time()
            self.f_time = stop_time - start_time
            time.sleep(0.05)

    def step(self):
        pilot_angle, pilot_throttle = self.pilot.decide(
            self.vision_sensor.frame)

        if self.record:
            self.recorder.record_frame(
                self.vision_sensor.frame, pilot_angle, pilot_throttle)

        if self.recorder.is_recording:
            self.indicator.set_state('recording')
        elif self.record:
            self.indicator.set_state('standby')
        else:
            self.indicator.set_state('ready')

        self.pilot_angle = pilot_angle
        self.pilot_throttle = pilot_throttle

        self.mixer.update(pilot_throttle, pilot_angle)

    def setup_pilots(self, model_path):
        # TODO: This should scan for pilot modules and add them
        # TODO: add logging
        keras = KerasCategorical(model_path)
        keras.load()
        self.pilots = []
        try:
            f710 = F710()
            mixedf710 = MixedF710(keras, f710)
            self.pilots.append(f710)
            self.pilots.append(mixedf710)
        except Exception as e:
            print "Unable to load F710 Gamepad"
            print e
        try:
            rc = RC()
            mixedrc = MixedRC(keras, rc)
            self.pilots.append(rc)
            self.pilots.append(mixedrc)
        except Exception as e:
            print "Unable to load RC"
            print e

        self.pilot = self.pilots[0]
        self.pilot_yaw = 0
        self.pilot_throttle = 0

    def setup_recorders(self):
        self.recorder = FileRecorder()
        self.record = False

    def setup_mixers(self):
        self.th_pwm = NAVIO2PWM(2)
        self.st_pwm = NAVIO2PWM(0)
        self.mixer = AckermannSteeringMixer(
            steering_driver=self.st_pwm, 
            throttle_driver=self.th_pwm)

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
