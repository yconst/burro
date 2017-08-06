import os
import sys
from generators.file_generators import filename_generator

import numpy as np

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import methods

def angles_histogram(image_dir):
    '''
    Accepts a path and generates a histogram based on all angles
    of training file in path.
    '''
    angles = []
    for _, angle in filename_generator(image_dir):
        angles.append(angle)
    return np.histogram(angles)
