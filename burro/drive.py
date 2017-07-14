"""
drive.py

Starts a driving loop

Usage:
    drive.py [--vision=<name>]

Options:
  --vision=<name>     vision sensor type [default: camera]
"""

import sys
import time

from docopt import docopt

import methods
import config

from sensors import PiVideoStream
from models import list_models
from pilots import (KerasCategorical, 
    RC, F710, MixedRC, MixedF710)
from mixers import AckermannSteeringMixer
from drivers import NAVIO2PWM
from indicators import NAVIO2LED
from remotes import WebRemote
from recorders import FileRecorder

import logging

class Rover(object):

    def __init__(self):
        self.f_time = 0.
        arguments = docopt(__doc__)
        self.setup_pilots()
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
            time.sleep(max(0.01, 0.05 - self.f_time))

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

    def setup_pilots(self):
        self.pilots = []
        try:
            f710 = F710()
            self.pilots.append(f710)
        except Exception as e:
            f710 = None
            logging.info("Unable to load F710 Gamepad")
        try:
            rc = RC()
            self.pilots.append(rc)
        except Exception as e:
            rc = None
            logging.info("Unable to load RC")
        model_paths = list_models()
        for model_path, model_name in model_paths:
            keras = KerasCategorical(model_path, name=model_name)
            logging.info("Loading model " + model_name)
            keras.load()
            if f710:
                self.pilots.append(MixedF710(keras, f710))
            if rc:
                self.pilots.append(MixedRC(keras, rc))

        self.pilot = self.pilots[0]
        self.pilot_yaw = 0.
        self.pilot_throttle = 0.

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
