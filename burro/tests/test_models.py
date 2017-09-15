import sys
import os
import unittest
import numpy as np

from models import list_models
 
class TestModels(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_list_models(self):
        file = sys.modules[__name__].__file__
        path = os.path.dirname(os.path.realpath(file))
        f = open(os.path.join(path, "../models/unit_test.h5"), "a")
        models_list = list_models()
        self.assertTrue(models_list)

 
if __name__ == '__main__':
    unittest.main()

