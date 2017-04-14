'''

pilots.py

Methods to create, use, save and load pilots. Pilots 
contain the highlevel logic used to determine the angle
and throttle of a vehicle. Pilots can include one or more 
models to help direct the vehicles motion. 

'''
from __future__ import division

import os
import math
import random
from operator import itemgetter
from datetime import datetime

import numpy as np
import keras

from navio import leds

import methods

class BasePilot(object):
    '''
    Base class to define common functions.
    When creating a class, only override the funtions you'd like to replace.
    '''
    def __init__(self, name=None, last_modified=None):
        self.led = leds.Led()
        self.name = name
        self.last_modified = last_modified

    def decide(self, img_arr):
        angle = 0.0
        speed = 0.0
        return angle, speed

    def load(self):
        pass

    def pname(self):
        return "Default"


class KerasCategorical(BasePilot):
    def __init__(self, model_path, **kwargs):
        self.model_path = model_path
        self.model = None #load() loads the model
        super(KerasCategorical, self).__init__(**kwargs)

    def decide(self, img_arr):
        self.led.setColor('Green')
        img_arr = img_arr.reshape((1,) + img_arr.shape)
        angle_binned, throttle = self.model.predict(img_arr)
        angle_certainty = max(angle_binned[0])
        angle_unbinned = methods.unbin_Y(angle_binned)
        return angle_unbinned[0], throttle[0][0] * 0.0

    def load(self):
        self.model = keras.models.load_model(self.model_path)

    def pname(self):
        return "Keras Categorical"

