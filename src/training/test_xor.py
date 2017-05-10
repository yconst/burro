import os
import glob
import math

import numpy as np

from keras.models import Model, Sequential
from keras.layers import Input, Activation, Dense, Convolution2D, Dropout, Flatten
from keras.optimizers import SGD

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
    testtrain()
