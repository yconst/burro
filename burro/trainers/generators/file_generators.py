import os
import time
import glob

import methods
import config


def filename_generator(path, indefinite=False, signal_end=False):
    '''
    Generator that loops (indefinitely) through
    files and telemetry data embedded in file names.
    '''
    paths = glob.glob(os.path.join(path, '*.jpg'))
    if not paths:
        return
    while True:
        for file_path in paths:
            angle, throttle, ms = methods.parse_img_filepath(file_path)
            yield file_path, angle
        if not indefinite:
            break
        if signal_end:
            print "\nRestart Dataset\n"
