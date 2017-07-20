from __future__ import division

import numpy as np

import config

'''
BINNING
functions to help convert between floating point numbers and categories.
'''

def to_index(a, low=-1.0, high=1.0, bins=config.MODEL_OUTPUT_SIZE):
    step = (high - low) / bins
    b = min( int((a - low)/step), bins-1)
    return b

def from_index(b, low=-1.0, high=1.0, bins=config.MODEL_OUTPUT_SIZE):
    step = (high - low) / bins
    a = (b + 0.5) * step + low
    return a

def to_one_hot(y, low=-1.0, high=1.0, bins=config.MODEL_OUTPUT_SIZE):
    arr = np.zeros(config.MODEL_OUTPUT_SIZE)
    arr[to_index(y, low=low, high=high, bins=bins)] = 1
    return arr

def from_one_hot(y):
    v = np.argmax(y)
    v = from_index(v, low=low, high=high)
    return v


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
Image filepath
'''

def parse_img_filepath(filepath):
    '''
    Parse an image filename and derive angle
    and throttle values
    '''
    f = filepath.split('/')[-1]
    f = f[:-4] #remove ".jpg"
    f = f.split('_')

    throttle = float(f[3]) * 0.001
    angle = float(f[5]) * 0.1
    milliseconds = round(float(f[7]))

    return angle, throttle, milliseconds


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
