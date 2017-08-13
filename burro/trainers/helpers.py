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
from generators.misc_generators import angle_to_yaw

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

def categorical_pipeline(data_dir, mode, batch_size=32, val_every=10, offset=0):
    gen = filename_generator(data_dir, indefinite=True)
    gen = nth_select(gen, mode=mode, nth=val_every, offset=offset)
    #gen = equalize_probs(gen)
    gen = image_generator(gen)
    gen = image_mirror(gen)
    #gen = image_voffset(gen)
    gen = image_rotate(gen)
    gen = image_resize(gen)
    gen = image_crop(gen)
    gen = array_generator(gen)
    gen = center_normalize(gen)
    gen = brightness_shifter(gen, min_shift=-0.28, max_shift=0.18)
    gen = category_generator(gen)
    gen = batch_image_generator(gen, batch_size=batch_size)
    return gen

def regression_pipeline(data_dir, mode, batch_size=32, val_every=10, offset=0):
    gen = filename_generator(data_dir, indefinite=True)
    gen = nth_select(gen, mode=mode, nth=val_every, offset=offset)
    #gen = equalize_probs(gen)
    gen = image_generator(gen)
    gen = image_mirror(gen)
    #gen = image_voffset(gen)
    gen = image_rotate(gen)
    gen = image_resize(gen)
    gen = image_crop(gen)
    gen = array_generator(gen)
    gen = center_normalize(gen)
    gen = brightness_shifter(gen, min_shift=-0.28, max_shift=0.18)
    gen = angle_to_yaw(gen)
    gen = batch_image_generator(gen, batch_size=batch_size)
    return gen
