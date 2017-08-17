'''

pilots.py

Classes representing various CNN-based pilots.

'''
from __future__ import division

import os
import math
import random
from operator import itemgetter
from datetime import datetime

import numpy as np
import keras

import methods
from config import config


class BasePilot(object):
    '''
    Base class to define common functions.
    When creating a class, only override the funtions you'd like to replace.
    '''

    def __init__(self, name=None, last_modified=None):
        self.name = name
        self.last_modified = last_modified

    def decide(self, img_arr):
        return 0., 0.

    def pname(self):
        return self.name or "Default"


class KerasCategorical(BasePilot):
    '''
    A pilot based on a CNN with categorical output
    '''

    def __init__(self, model_path, **kwargs):
        self.yaw = 0
        self.model = keras.models.load_model(model_path)
        super(KerasCategorical, self).__init__(**kwargs)

    def decide(self, img_arr):
        if config.camera.crop_top or config.camera.crop_bottom:
            h, w, _ = img_arr.shape
            t = config.camera.crop_top
            l = h - config.camera.crop_bottom
            img_arr = img_arr[t:l, :]

        img_arr = np.interp(img_arr, config.camera.output_range,
                            config.model.input_range)
        img_arr = np.expand_dims(img_arr, axis=0)
        prediction = self.model.predict(img_arr)
        if len(prediction) == 2:
            yaw_binned = prediction[0]
            throttle = prediction[1][0][0]
        else:
            yaw_binned = prediction
            throttle = 0
        yaw = methods.from_one_hot(yaw_binned)

        avf = config.model.average_factor
        yaw = avf * self.yaw + (1.0 - avf) * yaw
        self.yaw = yaw
        return methods.yaw_to_angle(yaw), throttle * 0.15

    def pname(self):
        return self.name or "Keras Categorical"


class KerasRegression(BasePilot):
    '''
    A pilot based on a CNN with scalar output
    '''

    def __init__(self, model_path, **kwargs):
        self.yaw = 0
        self.model = keras.models.load_model(model_path)
        super(KerasRegression, self).__init__(**kwargs)

    def decide(self, img_arr):
        if config.camera.crop_top or config.camera.crop_bottom:
            h, w, _ = img_arr.shape
            t = config.camera.crop_top
            l = h - config.camera.crop_bottom
            img_arr = img_arr[t:l, :]

        img_arr = np.interp(img_arr, config.camera.output_range,
                            config.model.input_range)
        img_arr = np.expand_dims(img_arr, axis=0)
        prediction = self.model.predict(img_arr)
        if len(prediction) == 2:
            yaw = prediction[0]
            throttle = prediction[1]
        else:
            yaw = prediction
            throttle = 0

        avf = config.model.average_factor
        yaw = avf * self.yaw + (1.0 - avf) * yaw
        self.yaw = yaw
        return methods.yaw_to_angle(yaw), throttle * 0.15

    def pname(self):
        return self.name or "Keras Categorical"
