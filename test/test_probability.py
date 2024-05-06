import unittest

from src.probability import Normal


class TestProbability(unittest.TestCase):

    def test_neg_normal(self):
        x = Normal(1, 2)
        self.assertEqual(Normal(-2, 8), -2 * x)
        self.assertEqual(Normal(-2, 8), -(2 * x))
        self.assertEqual(Normal(-2, 8), x * -2)

    def test_normal_probability_with_number(self):
        x = Normal(2, 4)
        self.assertEqual((7, 4), ((5 + x).mu, (5 + x).sigma2))
        self.assertEqual((7, 4), ((x + 5).mu, (x + 5).sigma2))
        self.assertEqual((3, 4), ((5 - x).mu, (5 - x).sigma2))
        self.assertEqual((-3, 4), ((x - 5).mu, (x - 5).sigma2))

        self.assertEqual((4, 16), ((2 * x).mu, (2 * x).sigma2))
        self.assertEqual((4, 16), ((x * 2).mu, (x * 2).sigma2))
        self.assertEqual((1, 1), ((x / 2).mu, (x / 2).sigma2))

        self.assertEqual((2, 4), (x.mu, x.sigma2))

    def test_normal_probability_with_normal(self):
        x = Normal(1, 2)
        y = Normal(4, 12)

        z = x + y
        self.assertEqual(5, z.mu)
        self.assertEqual(14, z.sigma2)

        z = 10 + 3 * x - y / 2
        self.assertEqual(11, z.mu)
        self.assertEqual(21, z.sigma2)

    def test_hash_normal_probability(self):
        x = Normal(1, 2)
        y = Normal(4, 6)
        data = set()

        self.assertNotIn(x, data)
        self.assertNotIn(y, data)

        data.add(x)

        self.assertIn(x, data)
        self.assertNotIn(y, data)

        z = 3 + 2 * x

        data.add(z)

        self.assertIn(x, data)
        self.assertNotIn(y, data)

        data.add(x)

        self.assertIn(x, data)
        self.assertNotIn(y, data)

        data.add(y)

        self.assertIn(x, data)
        self.assertIn(y, data)

        data.remove(y)

        self.assertIn(x, data)
        self.assertNotIn(y, data)
