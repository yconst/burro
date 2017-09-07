import random

import numpy as np

import methods
from config import config


def category_generator(generator):
    '''
    Generator that yields categorical angle from scalar
    '''
    max_steering_angle = config.ackermann_car.max_steering_angle
    for inp, angle in generator:
        yield inp, methods.to_one_hot(angle,
                                      low=-max_steering_angle,
                                      high=max_steering_angle)


def brightness_shifter(generator, min_shift=-0.1, max_shift=0.1):
    '''
    Generator that shifts brightness of an np array
    '''
    for img_array, angle in generator:
        shift_value = random.uniform(min_shift, max_shift)
        shift = np.array([shift_value,
                          shift_value,
                          shift_value])
        img_out = np.clip(img_array + shift, -1.0, 0.9999)
        yield img_out, angle


def batch_image_generator(generator, batch_size=32):
    '''
    Generator that bundles images and telemetry into batches.
    '''
    X_b = []
    Y_b = []
    for X, Y in generator:
        X_b.append(X)
        Y_b.append(Y)
        if len(X_b) == batch_size:
            yield np.array(X_b), np.array(Y_b)
            X_b = []
            Y_b = []
    yield np.array(X_b), np.array(Y_b)


def center_normalize(generator):
    '''
    Generators that zero-centers and normalizes image data
    '''
    for X, Y in generator:
        X = X / 128.
        X = X - 1.  # zero-center
        yield X, Y


def equalize_probs(generator,
                   prob=config.training.equalize_prob_strength,
                   symmetric=config.training.symmetric):
    '''
    Generators that attempts to equalize the number of times
    each bin has appeared in the stream
    This could be done to accept bins instead of angles
    however it is more practical to place it early in the
    pipeline before the angle is converted to category
    '''
    size = config.model.output_size
    max_steering_angle = config.ackermann_car.max_steering_angle
    picks = np.ones(size)
    for inp, angle in generator:
        inp_idx = methods.to_index(angle,
                                   low=-max_steering_angle,
                                   high=max_steering_angle)
        pick_mean = np.mean(picks)
        if picks[inp_idx] > pick_mean and random.uniform(0, 1) < prob:
            continue
        picks[inp_idx] += 1
        if symmetric and inp_idx != size - inp_idx - 1:
            picks[size - inp_idx - 1] += 1
        yield inp, angle


def nth_select(generator, nth, mode='reject_nth', offset=0):
    '''
    Generator that either selects or discards nth input
    including offset
    '''
    assert(mode in ['accept_nth', 'reject_nth'])
    counter = 0
    for inp, angle in generator:
        is_nth = counter % nth == offset
        if (is_nth and mode == 'accept_nth' or
            not is_nth and mode == 'reject_nth'):
            yield inp, angle
        counter += 1


def gaussian_noise(generator, scale=config.training.noise_scale):
    '''
    Generator that adds gaussian noise to an 2d numpy
    array (an image)
    '''
    for inp, angle in generator:
        scale_instance = np.random.randn() * scale
        noisy = np.random.randn(*inp.shape) * scale_instance
        inp = np.clip(inp + noisy, -1.0, 0.9999)
        yield inp, angle
