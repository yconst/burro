'''

pilots.py

Classes representing base pilots.

'''

class BasePilot(object):
    '''
    Base class to define common functions.
    When creating a class, only override the funtions you'd like to replace.
    '''
    def __init__(self, name=None, last_modified=None):
        self.name = name
        self.last_modified = last_modified

    def decide(self, img_arr):
        return 0., 0.

    def pname(self):
        return self.name or "Default"


class TestPilot(BasePilot):
    '''
    Represents a pilot for testing inference
    '''
    def set_response(self, angle, throttle):
        self.angle = angle
        self.throttle = throttle

    def decide(self, img_arr):
        return self.angle, self.throttle