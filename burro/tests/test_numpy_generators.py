import unittest

import numpy as np

from trainers.generators import numpy_generators
import config


def normal_generator(angle = config.CAR_MAX_STEERING_ANGLE*0.5,
                     trim = config.CAR_MAX_STEERING_ANGLE):
    while True:
        rand = np.random.normal(0, angle)
        rand = min(trim, max(-trim, rand))
        yield "", rand

class EqualizeGeneratorTest(unittest.TestCase):
    def test(self):
        gen = normal_generator()
        gen = numpy_generators.equalize_probs(gen)
        vals = np.zeros(10000)
        for i in range(vals.size-1):
            _, vals[i] = next(gen)
        hist = np.histogram(vals)
        sd = np.std(hist[0])
        self.assertLess(sd, 100)

if __name__ == '__main__':
    unittest.main()
