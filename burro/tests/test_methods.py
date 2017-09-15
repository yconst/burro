import unittest
from methods import yaw_to_angle, angle_to_yaw
 
class TestMethods(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_angle_conversion(self):
        for yaw in range(-1, 1, 0.1):
        	test_yaw = yaw_to_angle(angle_to_yaw(yaw))
        	self.assertEqual(yaw, test_yaw)

 
if __name__ == '__main__':
    unittest.main()

