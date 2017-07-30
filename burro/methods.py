from __future__ import division

import os
import subprocess
import re

import numpy as np

import config

'''
BINNING
functions to help convert between floating point numbers and categories.
'''


def linear_bin(a, o=config.MODEL_OUTPUT_SIZE):
    a = a + 1
    b = round(a / (2 / (float(o) - 1.)))
    return int(b)


def linear_unbin(b, o=config.MODEL_OUTPUT_SIZE):
    a = b * (2 / (float(o) - 1.)) - 1
    return a


def bin_Y(Y, o=config.MODEL_OUTPUT_SIZE):
    d = []
    for y in Y:
        arr = np.zeros(o)
        arr[linear_bin(y)] = 1
        d.append(arr)
    return np.array(d)


def unbin_Y(Y):
    d = []
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
    return angle / float(limit)


def yaw_to_angle(yaw, limit=config.CAR_MAX_STEERING_ANGLE):
    '''
    Convert from yaw to angle
    '''
    return yaw * float(limit)


'''
I2C TOOLS
functions to help with discovering i2c devices
'''

def i2c_addresses(bus_index):
    '''
    Get I2C Addresses using i2cdetect. 
    Unfortunately the alternative, simpler implementation
    using smbus does not detect NAVIO2 properly, so it's
    needed that i2cdetect is called.
    '''
    addresses = []

    p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
    for i in range(0,9):
        line = str(p.stdout.readline())
        for match in re.finditer("[0-9][0-9]:.*[0-9][0-9]", line):
            for number in re.finditer("[0-9][0-9](?!:)", match.group()):
                addresses.append('0x' + number.group())
    return addresses
            

def board_type():
    '''
    Guess the available board type based on the
    I2C addresses found.
    '''
    addresses = i2c_addresses(1)
    if not addresses:
        return None
    if '0x77' in addresses:
        return 'navio'
    elif '0x60' in addresses:
        return 'adafruit'
