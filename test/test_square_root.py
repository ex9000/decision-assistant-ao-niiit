import unittest

from src.square_root import solve


class TestSquareRoot(unittest.TestCase):
    def test_square_root(self):
        x1, x2 = solve(-2, -4, 4)
        self.assertAlmostEqual(x1, -1 - 3**0.5, 10)
        self.assertAlmostEqual(x2, -1 + 3**0.5, 10)
