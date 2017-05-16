#-*- coding:utf-8 -*-

import time
import os

from PIL import Image

import config

CURRENT_MIL = lambda: int(round(time.time() * 1000))

class BaseRecorder(object):
    '''
    A base class for image/sensor recording devices
    '''
    def __init__(self):
        self.frame_count = 0
        self.is_recording = False

    def record_frame(self, image_array, angle, throttle):
        '''
        Accepts an image, angle and throttle values and
        records them. This is a proxy method
        '''
        pass


class FileRecorder(BaseRecorder):
    '''
    A class that records camera images and associated
    throttle and angle information.
    '''
    def __init__(self):
        self.instance_path = self.make_instance_dir(config.SESSION_DIR)
        super(FileRecorder, self).__init__()

    def make_instance_dir(self, sessions_path):
        '''
        Create a directory for the current session based on time,
        and a global sessions directory if it does not exist.
        '''
        if not os.path.isdir(sessions_path):
            os.makedirs(sessions_path)
        instance_name = time.strftime('%Y_%m_%d__%I_%M_%S_%p')
        instance_path = os.path.join(sessions_path, instance_name)
        if not os.path.isdir(instance_path):
            os.makedirs(instance_path)
        return instance_path

    def record_frame(self, image_array, angle, throttle):
        '''
        Record a single frame, with frame index, angle and throttle values
        as its filename
        '''
        # throttle is inversed, i.e. forward is negative, backwards positive
        # we are only interested in forward values of throttle
        # angle is counter-clockwise, i.e. left is positive
        # TODO: make a proper value mapping here, and then transform
        if throttle * -1.0 < config.THROTTLE_RECORD_LIMIT:
            self.is_recording = False
            return
        self.is_recording = True
        file_angle = int(angle*10)
        file_throttle = int(throttle * 1000)
        filepath = self.create_img_filepath(self.instance_path,
                                            self.frame_count,
                                            file_angle,
                                            file_throttle)
        img = Image.fromarray(image_array)
        img.save(filepath)
        self.frame_count += 1

    def create_img_filepath(self, directory, frame_count, angle, throttle):
        '''
        Generate the complete filepath for saving an image
        '''
        filepath = str("%s/" % directory + "frame_" + str(frame_count).zfill(5) + \
                        "_ttl_" + str(throttle) + "_agl_" + str(angle) + "_mil_" + \
                        str(CURRENT_MIL()) + '.jpg')
        return filepath
