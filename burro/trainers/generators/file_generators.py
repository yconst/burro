import os
import time
import fnmatch

import methods

def filename_generator(file_dir, indefinite=False, signal_end=False):
    '''
    Generator that loops (indefinitely) through
    files and telemetry data embedded in file names.
    '''
    paths = files(file_dir)
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

def files(file_dir, pattern='*.jpg'):
    import ipdb; ipdb.set_trace()
    matches = []
    for root, dirnames, filenames in os.walk(file_dir):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
        for sub_dir in dirnames:
            matches.extend(files(os.path.join(root, sub_dir), pattern))
    return matches

def file_count(file_dir):
    '''
    Accepts a path and returns the image count contained
    '''
    paths = files(file_dir)
    if not paths:
        return 0
    return len(paths)
