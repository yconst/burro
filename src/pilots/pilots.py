#-*- coding:utf-8 -*-

'''

pilots.py

Methods to create, use, save and load pilots. Pilots
contain the highlevel logic used to determine the angle
and throttle of a vehicle. Pilots can include one or more
models to help direct the vehicles motion.

'''
from __future__ import division

import keras

from navio import leds

import config
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
        '''
        Accepts an image and returns corresponding angle and throttle values.
        This is a dummy function.
        '''
        angle = 0.0
        throttle = 0.0
        return angle, throttle

    def pname(self):
        '''
        Returns the assigned name for this pilot subclass
        '''
        return "Default"


class KerasCategorical(BasePilot):
    '''
    A pilot using a Convolutional Neural Network with
    categorical output
    '''
    def __init__(self, model_path, **kwargs):
        self.model_path = model_path
        self.model = None #load() loads the model
        self.avg_factor = config.KERAS_AVERAGE_FACTOR
        self.yaw = 0
        self.model = keras.models.load_model(self.model_path)
        super(KerasCategorical, self).__init__(**kwargs)

    def decide(self, img_arr):
        self.led.setColor('Green')
        img_arr = img_arr.reshape((1,) + img_arr.shape)
        yaw_binned, throttle = self.model.predict(img_arr)
        #yaw_certainty = max(yaw_binned[0])
        yaw_unbinned = methods.unbin_Y(yaw_binned)

        yaw = yaw_unbinned[0]
        yaw = self.avg_factor * self.yaw + (1.0 - self.avg_factor) * yaw
        self.yaw = yaw
        throttle = throttle[0][0]
        return methods.yaw_to_angle(yaw), throttle * 0.15

    def pname(self):
        return "Keras Categorical"
