from __future__ import division

import os
<<<<<<< HEAD
import os.path
=======
import subprocess
import re

>>>>>>> db8fb8534c1565dfb5fb6ad867011af852a5f1dd
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
    v = from_index(v)
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
Filepaths
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

def create_file(path):
    '''
    Create a file at path if not exist
    '''
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def touch(fname):
        try:
            os.utime(fname, None)
        except OSError:
            open(fname, 'a').close()

    mkdir_p(os.path.dirname(path))
    touch(path)


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
