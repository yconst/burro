'''
mixers.py
Classes to wrap motor controllers into a functional drive unit.
'''

import methods
from config import config


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
        if not config.ackermann_car.reverse_steering:
            yaw = -yaw
        self.throttle_driver.update(throttle)
        self.steering_driver.update(yaw)


class DifferentialSteeringMixer(BaseMixer):
    '''
    Mixer for vehicles using differential steering.
    This mixer uses throttle-proportional steering so that the vehicle
    behaves more like a car rather than a robot.
    '''
    def __init__(self, left_driver, right_driver):
        self.left_driver = left_driver
        self.right_driver = right_driver

    def update(self, throttle, angle):
        throttle = min(1, max(-1, throttle))
        l_speed = (throttle - angle * throttle / 90.) * config.differential_car.left_mult
        r_speed = (throttle + angle * throttle / 90.) * config.differential_car.right_mult
        l_speed = min(max(l_speed, -1), 1)
        r_speed = min(max(r_speed, -1), 1)
        if config.differential_car.left_reverse:
            l_speed = -l_speed
        if config.differential_car.right_reverse:
            r_speed = -r_speed
        self.left_driver.update(l_speed)
        self.right_driver.update(r_speed)
