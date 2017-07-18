
import methods
import config

from rover import Rover
from sensors import PiVideoStream
from models import list_models
from pilots import (KerasCategorical, 
    RC, F710, MixedRC, MixedF710)
from mixers import AckermannSteeringMixer, DifferentialSteeringMixer
from drivers import NAVIO2PWM, Adafruit_MotorHAT
from indicators import Indicator, NAVIO2LED
from remotes import WebRemote
from recorders import FileRecorder

import logging

class Composer(object):
    
    def new_vehicle(self):
        rover = Rover()
        self.setup_pilots(rover)
        self.setup_recorders(rover)
        self.setup_mixers(rover)
        self.setup_remote(rover)
        self.setup_indicators(rover)
        self.setup_sensors(rover)
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

    def setup_mixers(self, rover):
        ready = False
        #try:
        #    throttle_driver = NAVIO2PWM(2)
        #    steering_driver = NAVIO2PWM(0)
        #    rover.mixer = AckermannSteeringMixer(
        #        steering_driver=steering_driver, 
        #        throttle_driver=throttle_driver)
        #    ready = True
        #except Exception:
           #logging.info("Unable to load NAVIO2 PWM")
        if ready == False:
            #try:
            left_driver = Adafruit_MotorHAT(1)
            right_driver = Adafruit_MotorHAT(2)
            rover.mixer = DifferentialSteeringMixer(
                left_driver=left_driver, 
                right_driver=right_driver)
            ready = True
            #except Exception:
            #    logging.info("Unable to load Motor HAT")
        if ready == False:
            logging.error("No drivers found - exiting")

    def setup_sensors(self, rover):
        rover.vision_sensor = PiVideoStream()

    def setup_remote(self, rover):
        rover.remote = WebRemote(rover)

    def setup_indicators(self, rover):
        try:
            rover.indicator = NAVIO2LED()
        except Exception:
            rover.indicator = Indicator()
