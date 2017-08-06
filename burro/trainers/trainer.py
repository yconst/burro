import os
import time

import numpy as np

from keras.models import Model, Sequential
from keras.layers import Input, Activation, Dense, Convolution2D, Dropout, Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard, ReduceLROnPlateau, ModelCheckpoint, EarlyStopping

import config
import methods
import helpers

from generators.file_generators import filename_generator
from generators.pil_generators import (image_count,
                            image_generator, image_flip, image_resize,
                            image_rotate, array_generator,
                            image_voffset)
from generators.numpy_generators import (category_generator,
                              brightness_shifter, batch_image_generator,
                              center_normalize, equalize_probs, nth_select)


def train(data_dir, track, optimizer='adam', patience=10, eq_prob=0.60):
    offset = 4

    gen_batch = 256
    val_batch = 32
    val_stride = 20

    dense1 = 150
    dense2 = 50

    now = time.strftime("%c")

    hist = helpers.angles_histogram(data_dir)
    print hist[0]
    print hist[1]

    model_dir = os.path.abspath(os.path.expanduser(config.MODELS_DIR))
    model_path = os.path.join(model_dir,
        'model-' + track + '-' + optimizer +
        '-' + str(dense1) + '-' + str(dense2) +
        '-' + now + '.h5')
    log_dir = os.path.abspath(os.path.expanduser(config.LOGS_DIR))
    log_path = os.path.join(log_dir,
    track + '/' + optimizer + '-' +
    str(dense1) + '-' + str(dense2) +
    '-' + now)

    methods.create_file(model_path)

    im_count = image_count(data_dir)
    gen = filename_generator(data_dir, indefinite=True)
    gen = nth_select(gen, mode='reject_nth', nth=10, offset=offset)
    gen = equalize_probs(gen, prob=eq_prob)
    gen = image_generator(gen)
    gen = image_flip(gen)
    gen = image_voffset(gen)
    gen = image_rotate(gen)
    gen = image_resize(gen)
    gen = array_generator(gen)
    gen = center_normalize(gen)
    gen = brightness_shifter(gen, min_shift=-0.28, max_shift=0.18)
    gen = category_generator(gen)
    gen = batch_image_generator(gen, batch_size=gen_batch)

    val = filename_generator(data_dir, indefinite=True)
    val = nth_select(val, mode='accept_nth', nth=10, offset=offset)
    val = equalize_probs(val, prob=eq_prob)
    val = image_generator(val)
    val = image_flip(val)
    val = image_voffset(val)
    val = image_rotate(val)
    val = image_resize(val)
    val = array_generator(val)
    val = center_normalize(val)
    val = brightness_shifter(val, min_shift=-0.2, max_shift=0.1)
    val = category_generator(val)
    val = batch_image_generator(val, batch_size=val_batch)

    model = Sequential()
    model.add(
        Convolution2D(
            24, (5, 5), strides=(
                2, 2), activation='relu', input_shape=(
                99, 132, 3)))
    model.add(Convolution2D(32, (5, 5), strides=(2, 2), activation='relu'))
    model.add(Convolution2D(64, (5, 5), strides=(2, 2), activation='relu'))
    model.add(Convolution2D(64, (3, 3), strides=(2, 2), activation='relu'))
    model.add(Convolution2D(24, (3, 3), strides=(1, 1), activation='relu'))
    model.add(Flatten())
    model.add(Dense(dense1, activation='relu'))
    #model.add( Dropout(.1) )
    model.add(Dense(dense2, activation='relu'))
    #model.add( Dropout(.1) )

    model.add(
        Dense(
            config.MODEL_OUTPUT_SIZE,
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

    hist = model.fit_generator(gen,
                               epochs=200,
                               steps_per_epoch=im_count / gen_batch,
                               validation_data=val,
                               validation_steps=im_count / (val_batch * val_stride),
                               callbacks=[tb, model_cp, e_stop])

    return np.min(hist.history['val_loss'])
