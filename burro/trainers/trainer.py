import os
import time

import numpy as np

from keras.models import Model, Sequential
from keras.layers import Input, Activation, Dense, Convolution2D, Dropout, Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard, ReduceLROnPlateau, ModelCheckpoint, EarlyStopping

from config import config
import methods

from generators import file_generators
import histograms
import img_pipelines


offset = 4

gen_batch = 256
val_batch = 32
val_stride = 20

dense1 = 100
dense2 = 50

now = time.strftime("%c")

def train_categorical(data_dir, track, optimizer='adam', patience=10):

    hist = histograms.angles_histogram(data_dir)
    print hist[0]
    print hist[1]

    input_shape=(99-config.camera.crop_top, 132, 3)
    print "Input shape: " + str(input_shape)

    models_dir = os.path.abspath(os.path.expanduser(config.training.models_dir))
    model_path = os.path.join(models_dir,
        'model-' + track + '-' + optimizer +
        '-' + str(dense1) + '-' + str(dense2) +
        '-' + now + '.h5')
    logs_dir = os.path.abspath(os.path.expanduser(config.training.logs_dir))
    log_path = os.path.join(logs_dir,
    track + '/' + optimizer + '-' +
    str(dense1) + '-' + str(dense2) +
    '-' + now)

    methods.create_file(model_path)

    im_count = file_generators.file_count(data_dir)
    gen = img_pipelines.categorical_pipeline(data_dir, mode='reject_nth',
        batch_size=gen_batch, offset=offset)
    val = img_pipelines.categorical_pipeline(data_dir, mode='accept_nth',
        batch_size=val_batch, offset=offset)

    model = Sequential()
    model.add(
        Convolution2D(
            24, (5, 5), strides=(
                2, 2), activation='relu', input_shape=input_shape))
    model.add(Convolution2D(32, (5, 5), strides=(2, 2), activation='relu'))
    model.add(Convolution2D(64, (5, 5), strides=(2, 2), activation='relu'))
    model.add(Convolution2D(64, (3, 3), strides=(1, 1), activation='relu'))
    model.add(Convolution2D(64, (2, 2), strides=(1, 1), activation='relu'))
    model.add(Flatten())
    model.add(Dense(dense1, activation='selu'))
    model.add( Dropout(.1) )
    model.add(Dense(dense2, activation='selu'))
    model.add( Dropout(.1) )

    model.add(
        Dense(
            config.model.output_size,
            activation='softmax',
            name='angle_out'))
    model.compile(
        optimizer=optimizer, loss={
            'angle_out': 'categorical_crossentropy'})

    print model.summary()

    tb = TensorBoard(log_path)
    # reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.96,
    #          patience=2, min_lr=0.0001)
    model_cp = ModelCheckpoint(model_path, monitor='val_loss',
                               save_best_only=True, mode='auto', period=1)
    e_stop = EarlyStopping(monitor='val_loss', patience=patience)

    print "Best model saved in " + model_path

    hist = model.fit_generator(gen,
                               epochs=200,
                               steps_per_epoch=im_count / gen_batch,
                               validation_data=val,
                               validation_steps=im_count / (val_batch * val_stride),
                               callbacks=[tb, model_cp, e_stop])

    return np.min(hist.history['val_loss'])

def train_regression(data_dir, track, optimizer='adam', patience=10):

    hist = histograms.angles_histogram(data_dir)
    print hist[0]
    print hist[1]

    input_shape=(99-config.camera.crop_top, 132, 3)
    print "Input shape: " + str(input_shape)

    models_dir = os.path.abspath(os.path.expanduser(config.training.models_dir))
    model_path = os.path.join(models_dir,
        'model-' + track + '-' + optimizer +
        '-' + str(dense1) + '-' + str(dense2) +
        '-' + now + '.h5')
    logs_dir = os.path.abspath(os.path.expanduser(config.training.logs_dir))
    log_path = os.path.join(logs_dir,
    track + '/' + optimizer + '-' +
    str(dense1) + '-' + str(dense2) +
    '-' + now)

    methods.create_file(model_path)

    im_count = file_generators.file_count(data_dir)
    gen = img_pipelines.regression_pipeline(data_dir, mode='reject_nth',
        batch_size=gen_batch, val_every=5, offset=offset)
    val = img_pipelines.regression_pipeline(data_dir, mode='accept_nth',
        batch_size=val_batch, val_every=5, offset=offset)

    model = Sequential()
    model.add(
        Convolution2D(
            24, (6, 6), strides=(
                2, 2), activation='relu', input_shape=input_shape))
    model.add(Convolution2D(32, (5, 5), strides=(2, 2), activation='relu'))
    model.add(Convolution2D(64, (5, 5), strides=(2, 2), activation='relu'))
    model.add(Convolution2D(64, (3, 3), strides=(1, 1), activation='relu'))
    model.add(Convolution2D(64, (2, 2), strides=(1, 1), activation='relu'))
    model.add(Flatten())
    model.add(Dense(dense1, activation='selu'))
    model.add( Dropout(.1) )
    model.add(Dense(dense2, activation='selu'))
    model.add( Dropout(.1) )

    model.add(Dense(1, activation='linear',name='angle_out'))
    model.compile(
        optimizer=optimizer, loss={
            'angle_out': 'mean_squared_error'})

    print model.summary()

    tb = TensorBoard(log_path)
    # reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.96,
    #          patience=2, min_lr=0.0001)
    model_cp = ModelCheckpoint(model_path, monitor='val_loss',
                               save_best_only=True, mode='auto', period=1)
    e_stop = EarlyStopping(monitor='val_loss', patience=patience)

    hist = model.fit_generator(gen,
                               epochs=200,
                               steps_per_epoch=im_count / gen_batch,
                               validation_data=val,
                               validation_steps=im_count / (val_batch * val_stride),
                               callbacks=[tb, model_cp, e_stop])

    min_val = np.min(hist.history['val_loss'])
    print "Best model: " + str(min_val)
    print "Saved in " + model_path

    return min_val
