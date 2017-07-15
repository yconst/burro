
from PIL import Image, ImageOps

import methods
import config


def gen_sin(generator):
    '''
    Generator that converts a steering angle to sinus
    '''
    for inp, angle in generator:
        yield inp, math.sin(math.radians(angle))
