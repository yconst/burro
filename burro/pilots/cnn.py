'''

cnn.py

Classes representing various CNN-based pilots.

'''

from __future__ import division

import numpy as np

import methods
from config import config

from pilot import BasePilot


class KerasCategorical(BasePilot):
    '''
    A pilot based on a CNN with categorical output
    '''

    def __init__(self, model_path, **kwargs):
        import keras

        self.yaw = 0
        self.throttle = 0
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
        else:
            yaw_binned = prediction
        yaw = methods.from_one_hot(yaw_binned)
        yaw_step = config.model.yaw_step
        if abs(yaw - self.yaw) < yaw_step:
            self.yaw = yaw
        elif yaw < self.yaw:
            yaw = self.yaw - yaw_step
        elif yaw > self.yaw:
            yaw = self.yaw + yaw_step
        self.yaw = yaw

        if len(prediction) == 2:
            throttle = prediction[1][0]
        else:
            throttle = (0.12 + np.amax(yaw_binned) * (1 - abs(yaw)) *
                       config.model.throttle_mult)
        avf_t = config.model.throttle_average_factor
        throttle = avf_t * self.throttle + (1.0 - avf_t) * throttle
        self.throttle = throttle
        
        return methods.yaw_to_angle(yaw), throttle * -1

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
            yaw = methods.angle_to_yaw(prediction[0][0])
            throttle = prediction[1][0]
        else:
            yaw = methods.angle_to_yaw(prediction[0][0])
            throttle = 0

        avf = config.model.yaw_average_factor
        yaw = avf * self.yaw + (1.0 - avf) * yaw
        self.yaw = yaw
        return methods.yaw_to_angle(yaw), throttle

    def pname(self):
        return self.name or "Keras Categorical"
