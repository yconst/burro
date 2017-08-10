import os
import time
import glob
import math
import random
from random import randint as ri

import numpy as np

from PIL import Image, ImageOps, ImageChops

import pyblur

import methods
from config import config

import logging


def image_generator(generator):
    '''
    Generator that yields images from files.
    '''
    for file_path, angle in generator:
        try:
            with Image.open(file_path) as img:
                angle, throttle, ms = methods.parse_img_filepath(file_path)
                yield img, angle
        except IOError as err:
            logging.warning(err)


def image_count(path):
    '''
    Accepts a path and returns the image count contained
    '''
    paths = glob.glob(os.path.join(path, '*.jpg'))
    if not paths:
        return 0
    return len(paths)


def image_crop(generator, top=config.camera.crop_top,
        bottom=config.camera.crop_bottom):
    '''
    Generator that crops the top pixels of an image
    '''
    for img, angle in generator:
        w, h = img.size
        yield img.crop((0, top, w, h-bottom)), angle


def image_resize(generator, size=config.camera.resolution):
    '''
    Generator that resizes images
    '''
    for img, angle in generator:
        img = img.resize(size, Image.ANTIALIAS)
        yield img, angle


def image_flip(generator):
    '''
    Generator that augments batches of images and telemetry
    through flipping
    '''
    for img, angle in generator:
        if random.uniform(0.0, 1.0) > 0.5:
            img = ImageOps.mirror(img)
            yield img, -angle
        yield img, angle


def image_rotate(generator, prob=0.4, max_angle=5):
    '''
    Generator that augments batches of images and telemetry
    through random rotation
    '''
    for img, input_angle in generator:
        if prob < random.uniform(0, 1):
            image_angle = random.uniform(-max_angle, max_angle)
            dst_im = Image.new(
                "RGBA", img.size, (ri(
                    0, 255), ri(
                    0, 255), ri(
                    0, 255)))
            rot = img.rotate(image_angle, expand=False)
            dst_im.paste(rot)
            img = dst_im.convert('RGB')
        yield img, input_angle


def image_voffset(generator, prob=0.4, max_pixels=5):
    '''
    Generator that vertically offsets an image
    '''
    for img, input_angle in generator:
        if prob < random.uniform(0, 1):
            image_offset = random.randrange(-max_pixels, max_pixels)
            dst_im = Image.new(
                "RGBA", img.size, (ri(
                    0, 255), ri(
                    0, 255), ri(
                    0, 255)))
            rot = ImageChops.offset(img, 0, image_offset)
            dst_im.paste(rot)
            img = dst_im.convert('RGB')
        yield img, input_angle


def array_generator(generator):
    '''
    Generator that yields a numpy array from a PIL image
    '''
    for img, outp in generator:
        yield np.array(img), outp
