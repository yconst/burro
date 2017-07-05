'''
mixers.py
Classes to wrap motor controllers into a functional drive unit.
'''

import config
import methods


class BaseMixer():

    def update(self, throttle=0, angle=0):
        '''
        Update steering angle and throttle of vehicle
        '''
        pass


class AckermannSteeringMixer(BaseMixer):
    '''
    Mixer for vehicles steered by changing the 
    angle of the front wheels.
    This is used for RC car-type vehicles.
    '''
    def __init__(self, 
                 steering_driver=None, 
                 throttle_driver=None):
        self.steering_driver = steering_driver
        self.throttle_driver = throttle_driver

    def update(self, throttle, angle):
        throttle = min(1, max(-1, -throttle))
        yaw = min(1, max(-1, methods.angle_to_yaw(angle)))

        if config.REVERSE_STEERING:
            yaw = -yaw

        self.throttle_driver.update(throttle)
        self.steering_driver.update(yaw)
        

class DifferentialSteeringMixer:
    """
    Mixer for vehicles using differential steering.
    """
    def __init__(self, left_driver, right_driver):
        self.left_driver = left_driver
        self.right_driver = right_driver
        self.angle=0
        self.throttle=0
    
    def update(self, throttle, angle):
        self.throttle = throttle
        self.angle = angle
        
        # TODO: convert from angle/throttle to driver value
        l_speed = ((self.left_driver.speed + throttle)/3 - angle/5)
        r_speed = ((self.right_driver.speed + throttle)/3 + angle/5)
        l_speed = min(max(l_speed, -1), 1)
        r_speed = min(max(r_speed, -1), 1)
        
        self.left_driver.turn(l_speed)
        self.right_driver.turn(r_speed)

