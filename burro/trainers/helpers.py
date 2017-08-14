import os
import sys
import glob
from generators.file_generators import filename_generator

import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import methods
from config import config

from generators.file_generators import filename_generator
from generators.pil_generators import (image_generator, image_mirror,
                            image_resize, image_rotate, array_generator,
                            image_voffset, image_crop)
from generators.numpy_generators import (category_generator,
                              brightness_shifter, batch_image_generator,
                              center_normalize, equalize_probs, nth_select)
from generators.misc_generators import angle_to_yaw, yaw_to_log

def image_count(path):
    '''
    Accepts a path and returns the image count contained
    '''
    paths = glob.glob(os.path.join(path, '*.jpg'))
    if not paths:
        return 0
    return len(paths)

def angles_histogram(image_dir):
    '''
    Accepts a path and generates a histogram based on all angles
    of training file in path.
    '''
    angles = []
    for _, angle in filename_generator(image_dir):
        angles.append(angle)
    return np.histogram(angles, config.model.output_size)

def categorical_pipeline(data_dir, mode='reject_nth', batch_size=32,
    prob=config.training.equalize_prob_strength, val_every=10, offset=0):
    '''
    Generate a pre-processing pipeline for a
    categorical output training problem.
    '''
    gen = filename_generator(data_dir, indefinite=True)
    if val_every > 0:
        gen = nth_select(gen, mode=mode, nth=val_every, offset=offset)
    if prob > 0:
        gen = equalize_probs(gen)
    gen = image_generator(gen)
    gen = image_mirror(gen)
    #gen = image_voffset(gen)
    gen = image_rotate(gen)
    gen = image_resize(gen)
    gen = image_crop(gen)
    gen = array_generator(gen)
    gen = center_normalize(gen)
    gen = brightness_shifter(gen)
    gen = category_generator(gen)
    if batch_size > 1:
        gen = batch_image_generator(gen, batch_size=batch_size)
    return gen

def regression_pipeline(data_dir, mode='reject_nth', batch_size=32,
    prob=config.training.equalize_prob_strength, val_every=10, offset=0):
    '''
    Generate a pre-processing pipeline for a
    regression training problem.
    '''
    gen = filename_generator(data_dir, indefinite=True)
    if val_every > 0:
        gen = nth_select(gen, mode=mode, nth=val_every, offset=offset)
    if prob > 0:
        gen = equalize_probs(gen)
    gen = image_generator(gen)
    gen = image_mirror(gen)
    #gen = image_voffset(gen)
    gen = image_rotate(gen)
    gen = image_resize(gen)
    gen = image_crop(gen)
    gen = array_generator(gen)
    gen = center_normalize(gen)
    gen = brightness_shifter(gen)
    gen = angle_to_yaw(gen)
    if batch_size > 1:
        gen = batch_image_generator(gen, batch_size=batch_size)
    return gen
