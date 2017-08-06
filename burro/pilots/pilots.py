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

import config, methods


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
        img_arr = np.interp(img_arr,config.CAMERA_OUTPUT_RANGE,
            config.MODEL_INPUT_RANGE)
        img_arr = np.expand_dims(img_arr, axis=0)
        prediction = self.model.predict(img_arr)
        if len(prediction) == 2:
            yaw_binned = prediction[0]
            throttle = prediction[1][0][0]
        else:
            yaw_binned = prediction
            throttle = 0
        yaw_unbinned = methods.from_one_hot(yaw_binned)

        yaw = yaw_unbinned[0]
        avf = config.KERAS_AVERAGE_FACTOR
        yaw = avf * self.yaw + (1.0 - avf) * yaw
        self.yaw = yaw
        return methods.yaw_to_angle(yaw), throttle * 0.15

    def pname(self):
        return self.name or "Keras Categorical"
