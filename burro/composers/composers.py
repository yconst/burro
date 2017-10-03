import sys

import methods
from config import config

from rover import Rover
from sensors.cameras import PiVideoStream
from models import list_models
from pilots import (KerasRegression, KerasCategorical,
                    RC, F710, MixedRC, MixedF710)
from mixers import AckermannSteeringMixer, DifferentialSteeringMixer
from drivers import NAVIO2PWM, NavioPWM, Adafruit_MotorHAT
from indicators import Indicator, NAVIO2LED
from remotes import WebRemote
from recorders import FileRecorder

import logging


class Composer(object):

    def new_vehicle(self, type=config.car.type):
        rover = Rover()
        self.board_type = methods.board_type()
        self.log_board_type()
        self.setup_pilots(rover)
        self.setup_recorders(rover)
        self.setup_mixers(rover, type)
        self.setup_remote(rover)
        self.setup_indicators(rover)
        self.setup_sensors(rover)
        return rover

    def log_board_type(self):
        if (self.board_type is 'navio'):
            logging.info("Found NAVIO+ HAT")
        elif (self.board_type is 'navio2'):
            logging.info("Found NAVIO2 HAT")
        elif (self.board_type is 'adafruit'):
            logging.info("Found Adafruit Motor HAT")

    def setup_pilots(self, rover):
        pilots = []
        try:
            f710 = F710()
            pilots.append(f710)
            logging.info("Loaded F710 Gamepad module")
        except Exception as e:
            f710 = None
        if self.board_type is 'navio':
            #Cant get RC for Navio to work yet
            pass
        elif self.board_type is 'navio2':
            rc = RC()
            pilots.append(rc)
            logging.info("Loaded RC module")
        else:
            rc = None
        model_paths = list_models()
        for model_path, model_name in model_paths:
            logging.info("Loading model " + model_name)
            keras = KerasCategorical(model_path, name=model_name)
            if f710:
                pilots.append(MixedF710(keras, f710))
            if rc:
                pilots.append(MixedRC(keras, rc))
        rover.pilots = pilots
        rover.set_pilot(0)

    def setup_recorders(self, rover):
        rover.recorder = FileRecorder()

    def setup_mixers(self, rover, type):
        if self.board_type is 'navio':
            logging.info("Setting up Ackermann car")
            throttle_driver = NavioPWM(config.ackermann_car_navio.throttle_channel)
            steering_driver = NavioPWM(config.ackermann_car_navio.steering_channel)
            rover.mixer = AckermannSteeringMixer(
                steering_driver=steering_driver,
                throttle_driver=throttle_driver)

        elif self.board_type is 'navio2':
            if type == 'differential':
                logging.info("Setting up differential car")
                left_driver = NAVIO2PWM(config.differential_car.left_channel)
                right_driver = NAVIO2PWM(config.differential_car.right_channel)
                rover.mixer = DifferentialSteeringMixer(
                    left_driver=left_driver,
                    right_driver=right_driver)
            else:
                logging.info("Setting up Ackermann car")
                throttle_driver = NAVIO2PWM(
                    config.ackermann_car.throttle_channel)
                steering_driver = NAVIO2PWM(
                    config.ackermann_car.steering_channel)
                rover.mixer = AckermannSteeringMixer(
                    steering_driver=steering_driver,
                    throttle_driver=throttle_driver)
        elif self.board_type is 'adafruit':
            logging.info("Setting up differential car")
            left_driver = Adafruit_MotorHAT(
                config.differential_car.left_channel + 1)
            right_driver = Adafruit_MotorHAT(
                config.differential_car.right_channel + 1)
            rover.mixer = DifferentialSteeringMixer(
                left_driver=left_driver,
                right_driver=right_driver)
        else:
            logging.error("No drivers found - exiting")
            sys.exit()

    def setup_sensors(self, rover):
        rover.vision_sensor = PiVideoStream()

    def setup_remote(self, rover):
        rover.remote = WebRemote(rover)

    def setup_indicators(self, rover):
        if self.board_type is 'navio2':
            rover.indicator = NAVIO2LED()
        else:
            rover.indicator = Indicator()
