
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
    '''
    for inp, angle in generator:
        yield inp, float(angle)/config.ackermann_car.max_steering_angle
