import math

from PIL import Image, ImageOps

import methods
from config import config


def angle_to_sin(generator):
    '''
    Generator that converts a steering angle to sinus
    '''
    for inp, angle in generator:
        yield inp, math.sin(math.radians(angle))

def angle_to_yaw(generator):
    '''
    Generator that converts angle values to yaw [-1, 1]
    '''
    for inp, angle in generator:
        yield inp, float(angle)/config.ackermann_car.max_steering_angle

def yaw_to_log(generator):
    '''
    Generator that log scales yaw values in the same range
    '''
    for inp, yaw in generator:
        yield inp, math.copysign(math.log((abs(yaw)+1)*9, 10), yaw)
