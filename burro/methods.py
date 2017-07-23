from __future__ import division

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
    import smbus

    bus = smbus.SMBus(bus_index)
    addresses = []

    for device in range(128):
          try:
             bus.read_byte(device)
             addresses.append(hex(device))
          except: # exception if read_byte fails
             pass
    return addresses

def board_type():
    addresses = i2c_addresses(1)
    if '0x48' in addresses and '0x77' in addresses:
        return 'navio'
    elif '0x60' in addresses:
        return 'adafruit'
