import os
import glob
import math

import numpy as np

from keras.models import Model, Sequential
from keras.layers import Input, Activation, Dense, Convolution2D, Dropout, Flatten
from keras.optimizers import SGD

from PIL import Image

def image_generator(path, indefinite=False):
    '''
    Generator that loops (indefinitely) through
    image arrays and their telemetry data.
    '''
    paths = glob.glob(os.path.join(path, '*.jpg'))
    while True:
        for file_path in paths:
            with Image.open(file_path) as img:
                img = img.resize((120, 120), Image.ANTIALIAS)
                img_arr = np.array(img)
                angle, throttle, ms = parse_img_filepath(file_path)
                yield img_arr, num_to_cat(angle)
        if not indefinite:
            break

def batch_image_generator(img_generator, batch_size=256):
    '''
    Generator that bundles images and telemetry into batches.
    '''
    X = []
    Y = []
    for img_arr, angle in img_generator:
        X.append(img_arr)
        Y.append(angle)
        if len(X) == batch_size:
            yield np.array(X), np.array(Y)
            X = []
            Y = []
    yield np.array(X), np.array(Y)

def num_to_cat(value, low=-1.0, high=1.0, bins=15):
    cat = np.zeros(bins)
    pos = int(round( (value - low)/(high - low) * bins ))
    cat[pos] = 1
    return cat

def parse_img_filepath(filepath):
    f = filepath.split('/')[-1]
    f = f[:-4] #remove ".jpg"
    f = f.split('_')

    throttle = round(float(f[3]), 2) / 1000.0
    angle = round(float(f[5]), 2) / 500.0 - 1.0
    milliseconds = round(float(f[7]))

    return angle, throttle, milliseconds

def train(train_folder):
    igen = image_generator(train_folder, indefinite=True)
    bgen = batch_image_generator(igen)

    model = Sequential()
    model.add( Convolution2D(24, (5, 5), strides=(2, 2), activation='relu', input_shape=(120,120,3)) )
    model.add( Convolution2D(32, (5, 5), strides=(2, 2), activation='relu') )
    model.add( Convolution2D(64, (5, 5), strides=(2, 2), activation='relu') )
    model.add( Convolution2D(64, (3, 3), strides=(2, 2), activation='relu') )
    model.add( Convolution2D(24, (3, 3), strides=(1, 1), activation='relu') )
    model.add( Flatten() )
    model.add( Dense(100, activation='relu') )
    model.add( Dropout(.1) )
    model.add( Dense(50, activation='relu') )
    model.add( Dropout(.1) )
    model.add( Dense(15, activation='softmax', name='angle_out') )
    model.compile(optimizer='rmsprop', loss={'angle_out': 'categorical_crossentropy'})
    print model.summary()

    model.fit_generator(bgen, epochs=10, steps_per_epoch=100)

if __name__ == "__main__":
    train('../../car_sessions/combined/')
