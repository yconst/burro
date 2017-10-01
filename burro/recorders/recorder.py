

class BaseRecorder(object):
    '''
    A base class for all recorders
    '''

    def __init__(self):
        self.frame_count = 0
        self.is_recording = False

    def record_frame(self, image_array, angle, throttle):
        '''
        Record a single image frame
        '''
        pass


class DummyRecorder(BaseRecorder):
    '''
    Represents a dummy recorder for testing
    '''
    pass
