from __future__ import division

import numpy as np

import config

'''
BINNING
functions to help convert between floating point numbers and categories.
'''

def linear_bin(a):
    a = a + 1
    b = round(a / (2/14))
    return int(b)

def linear_unbin(b):
    a = b *(2/14) - 1
    return a


def bin_Y(Y):
    d = []
    for y in Y:
        arr = np.zeros(15)
        arr[linear_bin(y)] = 1
        d.append(arr)
    return np.array(d) 
        
def unbin_Y(Y):
    d=[]
    for y in Y:
        v = np.argmax(y)
        v = linear_unbin(v)
        d.append(v)
    return np.array(d)

'''
ANGLE CONVERSIONS
functions to help converting between angles and yaw input values.
'''

def angle_to_yaw(angle, limit=config.CAR_MAX_STEERING_ANGLE):
    '''
    Convert from angle to yaw
    '''
    return yaw / float(limit)

def yaw_to_angle(yaw, limit=config.CAR_MAX_STEERING_ANGLE):
    '''
    Convert from yaw to angle
    '''
    return angle * float(limit)
