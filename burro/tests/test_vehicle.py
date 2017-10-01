import sys
import os
import unittest
import numpy as np
import random

from config import config

from pilots import TestPilot
from mixers import AckermannSteeringMixer, DifferentialSteeringMixer
from drivers import TestDriver
from recorders import DummyRecorder
from sensors import TestCamera
from indicators import DummyIndicator
from rover import Rover


class TestAckermannVehicle(unittest.TestCase):
 
    def setUp(self):
        vehicle = Rover()

        vehicle.pilots = [TestPilot()]
        vehicle.set_pilot(0)

        ds = TestDriver()
        dt = TestDriver()
        mx = AckermannSteeringMixer(throttle_driver=dt, steering_driver=ds)
        vehicle.mixer = mx

        vehicle.recorder = DummyRecorder()

        vehicle.vision_sensor = TestCamera()

        vehicle.indicator = DummyIndicator()

        self.vehicle = vehicle

    def test_vehicle_pipeline(self):
    	angle = random.uniform(-1.0, 1.0) * config.car.max_steering_angle
    	th = random.uniform(-1.0, 1.0)
    	
    	th_out = -th
    	st_out = -angle / config.car.max_steering_angle
    	if config.car.reverse_steering:
    		st_out = -st_out

    	self.vehicle.pilot.set_response(angle,th)
    	self.vehicle.step()

        self.assertAlmostEqual(self.vehicle.mixer.throttle_driver.output,
        	th_out, places=5)
        self.assertAlmostEqual(self.vehicle.mixer.steering_driver.output,
        	st_out, places=5)


class TestDifferentialVehicle(unittest.TestCase):
 
    def setUp(self):
        vehicle = Rover()

        vehicle.pilots = [TestPilot()]
        vehicle.set_pilot(0)

        d1 = TestDriver()
        d2 = TestDriver()
        mx = DifferentialSteeringMixer(left_driver=d1, right_driver=d2)
        vehicle.mixer = mx

        vehicle.recorder = DummyRecorder()

        vehicle.vision_sensor = TestCamera()

        vehicle.indicator = DummyIndicator()

        self.vehicle = vehicle

    def test_vehicle_pipeline(self):
    	th = random.uniform(-1.0, 1.0)
    	angle = random.uniform(-1.0, 1.0) * config.car.max_steering_angle

    	l_out = (th - angle * th / 90.) * config.differential_car.left_mult
        r_out = (th + angle * th / 90.) * config.differential_car.right_mult
        l_out = min(max(l_out, -1), 1)
        l_out = min(max(l_out, -1), 1)

    	self.vehicle.pilot.set_response(angle,th)
    	self.vehicle.step()

        self.assertAlmostEqual(self.vehicle.mixer.left_driver.output,
        	l_out, places=5)
        self.assertAlmostEqual(self.vehicle.mixer.right_driver.output,
        	r_out, places=5)
        

if __name__ == '__main__':
    unittest.main()
