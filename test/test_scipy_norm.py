import unittest
import scipy as sp


class TestScipyNorm(unittest.TestCase):
    def test_scipy_norm(self):
        dist = sp.stats.norm(10, 5)
        self.assertAlmostEqual(dist.mean(), 10, 10)
        self.assertEqual(dist.std(), 5, 10)
