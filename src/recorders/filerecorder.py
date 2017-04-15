
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
        sessions_path = os.path.dirname(config.SESSION_DIR)
        self.instance_path = self.make_instance_dir(sessions_path)
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
        if throttle < config.THROTTLE_RECORD_LIMIT:
            return
        file_yaw = int((yaw + 1) * 500)
        file_throttle = int((throttle + 1) * 500)
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


# if __name__ == "__main__":
#     import numpy

#     im = Image.open('/Users/yanconst/Temp/bg.jpg')

#     imarray = numpy.array(im)

#     fr = FileRecorder()

#     fr.record_frame(imarray, 0.15, 0.44)
#     fr.record_frame(imarray, 0.13, 0.54)
#     fr.record_frame(imarray, 0.16, 0.34)
#     fr.record_frame(imarray, 0.12, 0.74)
#     fr.record_frame(imarray, 0.13, 0.64)
#     fr.record_frame(imarray, 0.19, 0.54)


