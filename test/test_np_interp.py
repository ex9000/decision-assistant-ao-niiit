import unittest
import numpy as np


class TestNPInterp(unittest.TestCase):
    def test_np_interp(self):
        x: float = np.interp(1, (-2, 2), (-6, 6))
        self.assertAlmostEqual(x, 3.0, 10)
