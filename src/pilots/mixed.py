#-*- coding:utf-8 -*-

'''

mixed.py

Methods to create, use, save and load pilots. Pilots
contain the highlevel logic used to determine the angle
and throttle of a vehicle. Pilots can include one or more
models to help direct the vehicles motion.

'''

from rc import RC
from pilots import BasePilot, KerasCategorical

class Mixed(BasePilot):
    '''
    A mixed pilot using CNN for angle and RC for throttle
    '''
    def __init__(self, model_path, **kwargs):
        self.rc_pilot = RC()
        self.keras_pilot = KerasCategorical(model_path)
        super(Mixed, self).__init__(**kwargs)

    def decide(self, img_arr):
        _, rc_throttle = self.rc_pilot.decide(img_arr)
        keras_angle, _ = self.keras_pilot.decide(img_arr)
        return keras_angle, rc_throttle

    def pname(self):
        return "Mixed (Keras Cat. (angle) + RC (throttle))"
