
import methods
import config

from rover import Rover
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

class Composer(object):
	
	def compose_vehicle(self):
		rover = new Rover()
		self.setup_pilots(rover)
        self.setup_recorders(rover)
        self.setup_mixers(rover)
        self.set_sensors(rover, arguments['--vision'])
        self.set_remote(rover)
		
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

    def setup_recorders(self):
        self.recorder = FileRecorder()

    def setup_mixers(self):
        self.th_pwm = NAVIO2PWM(2)
        self.st_pwm = NAVIO2PWM(0)
        self.mixer = AckermannSteeringMixer(
            steering_driver=self.st_pwm, 
            throttle_driver=self.th_pwm)

    def set_sensors(self, vision_sensor):
        if vision_sensor == 'camera':
            self.vision_sensor = PiVideoStream()

    def set_remote(self):
        self.remote = WebRemote(self)
