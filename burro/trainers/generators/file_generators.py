import os
import time
import glob

import methods


def filename_generator(file_dir, indefinite=False, signal_end=False):
    '''
    Generator that loops (indefinitely) through
    files and telemetry data embedded in file names.
    '''
    paths = glob.glob(os.path.join(file_dir, '*.jpg'))
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
