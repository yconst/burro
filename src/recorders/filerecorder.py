
import time
import os

from PIL import Image

import config

current_milli_time = lambda: int(round(time.time() * 1000))

class BaseRecorder(object):
    
    def record_frame(self, image_array, yaw, throttle):
        pass
        

class FileRecorder(BaseRecorder):

    def __init__(self):
        self.instance_path = self.make_instance_dir(config.SESSION_DIR)
        self.frame_count = 0

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

    def record_frame(self, image_array, yaw, throttle):
        '''
        Record a single frame, with frame index, yaw and throttle values
        as its filename
        '''
        # throttle is inversed, i.e. forward is negative, backwards positive
        # we are only interested in forward values of throttle
        # yaw ir counter-clockwise, i.e. left is positive
        # TODO: make a proper value mapping here, and then transform
        if throttle * -1.0 < config.THROTTLE_RECORD_LIMIT:
            return
        file_yaw = int((yaw + 1) * 500)
        file_throttle = int(throttle * 1000)
        filepath = self.create_img_filepath(self.instance_path, self.frame_count, file_yaw, file_throttle)
        im = Image.fromarray(image_array)
        im.save(filepath)
        self.frame_count += 1

    def create_img_filepath(self, directory, frame_count, yaw, throttle):
        '''
        Generate the complete filepath for saving an image
        '''
        filepath = str("%s/" % directory + "frame_" + str(frame_count).zfill(5) + "_ttl_" + str(throttle) + "_agl_" + str(yaw) + "_mil_" + str(current_milli_time()) + '.jpg')
        return filepath
