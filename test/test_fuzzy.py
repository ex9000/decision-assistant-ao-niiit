import unittest

from src.fuzzy import TriangleSymmetric, Measure
from src.probability import Normal


class TestFuzzy(unittest.TestCase):
    def test_fuzzy(self):
        x = Normal(1, 2)
        y = Normal(3, 4)
        z = TriangleSymmetric(5, 6)

        x *= 2
        y *= 3
        z = 3 * (z - 1)

        r = x + z * y
        self.assertIsNotNone(r)
        self.assertEqual(Normal(29.0, 332.0), r.to_random(0, Measure.NECESSITY))
