
import methods
import config

from rover import Rover
from sensors import PiVideoStream
from models import list_models
from pilots import (KerasCategorical, 
    RC, F710, MixedRC, MixedF710)
from mixers import AckermannSteeringMixer
from drivers import NAVIO2PWM
from indicators import Indicator, NAVIO2LED
from remotes import WebRemote
from recorders import FileRecorder

import logging

class Composer(object):
    
    def new_vehicle(self):
        rover = Rover()
        self.setup_pilots(rover)
        self.setup_recorders(rover)
        self.setup_drivers(rover)
        self.setup_mixers(rover)
        self.setup_sensors(rover)
        self.setup_remote(rover)
        self.setup_indicators(rover)
        return rover
        
    def setup_pilots(self, rover):
        pilots = []
        try:
            f710 = F710()
            pilots.append(f710)
        except Exception as e:
            f710 = None
            logging.info("Unable to load F710 Gamepad")
        try:
            rc = RC()
            pilots.append(rc)
        except Exception as e:
            rc = None
            logging.info("Unable to load RC")
        model_paths = list_models()
        for model_path, model_name in model_paths:
            keras = KerasCategorical(model_path, name=model_name)
            logging.info("Loading model " + model_name)
            keras.load()
            if f710:
                pilots.append(MixedF710(keras, f710))
            if rc:
                pilots.append(MixedRC(keras, rc))
        rover.pilots = pilots
        rover.set_pilot(0)

    def setup_recorders(self, rover):
        rover.recorder = FileRecorder()

    def setup_drivers(self, rover):
        rover.th_pwm = NAVIO2PWM(2)
        rover.st_pwm = NAVIO2PWM(0)

    def setup_mixers(self, rover):
        rover.mixer = AckermannSteeringMixer(
            steering_driver=rover.st_pwm, 
            throttle_driver=rover.th_pwm)

    def setup_sensors(self, rover):
        rover.vision_sensor = PiVideoStream()

    def setup_remote(self, rover):
        rover.remote = WebRemote(rover)

    def setup_indicators(self, rover):
        try:
            rover.indicator = NAVIO2LED()
        except Exception:
            rover.indicator = Indicator()
