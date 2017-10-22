import unittest
import numpy as np

from methods import (yaw_to_angle, angle_to_yaw,
                     from_index, to_index,
                     to_one_hot, from_one_hot)


class TestMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_angle_conversion(self):
        for yaw in np.arange(-1, 1, 0.1):
            test_yaw = yaw_to_angle(angle_to_yaw(yaw))
            self.assertAlmostEqual(yaw, test_yaw, places=8)

    def test_binning_conversion(self):
        for val in np.arange(-1, 1, 0.1):
            test_val = from_index(to_index(val))
            self.assertTrue(abs(val - test_val) < 0.15)

    def test_one_hot_conversion(self):
        for val in np.arange(-1, 1, 0.1):
            test_oh = to_one_hot(val)
            test_val = from_one_hot(test_oh)
            self.assertTrue(abs(val - test_val) < 0.2)


if __name__ == '__main__':
    unittest.main()
