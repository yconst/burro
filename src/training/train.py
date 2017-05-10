import os
import glob
import math

import numpy as np

from keras.models import Model, Sequential
from keras.layers import Input, Activation, Dense, Convolution2D, Dropout, Flatten
from keras.optimizers import SGD

from PIL import Image

def images_to_arrays(path):
    '''
    '''
    X = []
    Y = []

    for file_path in glob.glob(os.path.join(path, '*.jpg')):
        with Image.open(file_path) as img:
            img = img.resize((120, 120), Image.ANTIALIAS)
            img_arr = np.array(img)
            angle, throttle, ms = parse_img_filepath(file_path)
            X.append(img_arr)
            Y.append(num_to_cat(angle))

    return np.array(X), np.array(Y)

def dataset_to_hdf5(X, Y, file_path):
    print('Saving HDF5 file to %s' %file_path)
    f = h5py.File(file_path, "w")
    f.create_dataset("X", data=X)
    f.create_dataset("Y", data=Y)
    f.close()

def num_to_cat(value, low=-1.0, high=1.0, bins=15):
    cat = np.zeros(bins)
    pos = int(round( (value - low)/(high - low) * bins ))
    cat[pos] = 1
    return cat

def parse_img_filepath(filepath):
    '''
    '''
    f = filepath.split('/')[-1]
    f = f[:-4] #remove ".jpg"
    f = f.split('_')

    throttle = round(float(f[3]), 2) / 1000.0
    angle = round(float(f[5]), 2) / 500.0 - 1.0
    milliseconds = round(float(f[7]))

    return angle, throttle, milliseconds
    #data = {'throttle':throttle, 'angle':angle, 'milliseconds': milliseconds}
    #return data

def train():
    X, Y = images_to_arrays('../../car_sessions/test/')

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
    model.fit(X, Y)

def testtrain():
    X = np.array([[0,1], [1,1], [0,0], [1,0]])
    Y = np.array([[1],[0],[0],[1]])

    model = Sequential()
    model.add(Dense(8, input_dim=2))
    model.add(Activation('tanh'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    sgd = SGD(lr=0.3)
    model.compile(loss='binary_crossentropy', optimizer=sgd)

    model.fit(X, Y, batch_size=4, nb_epoch=200)

    px = np.array([[0,1]])
    model.predict(x=px)

if __name__ == "__main__":
    train()
