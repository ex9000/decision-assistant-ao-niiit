import unittest

from src.fuzzy import TriangleSymmetric, Measure
from src.probability import Normal


class TestFuzzy(unittest.TestCase):
    def test_fuzzy(self):
        x = Normal(1, 2)
        y = Normal(3, 4)
        z = TriangleSymmetric(0, 1)

        x *= 2
        y *= 3
        z = 2 * (z + 1)

        r = x + z * y
        self.assertIsNotNone(r)
        self.assertEqual(Normal(11.0, 188.0), r.to_random(1, Measure.NECESSITY))
