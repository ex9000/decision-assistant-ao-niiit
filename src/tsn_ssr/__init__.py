"""Triangle Symmetric Normal Distribution Shift Scale Representation"""

import numpy as np

from src.fuzzy import TriangleSymmetric
from src.probability import Normal


def expected_as_polynomial(tsn: TriangleSymmetric[Normal]) -> np.ndarray:
    const = tsn.mode
    coeff = tsn.fuzziness / 2

    if tsn.scale is not None:
        const *= tsn.scale.mu
        coeff *= tsn.scale.mu

    # DO NOT MOVE ANYTHING ABOVE THIS LINE
    # ADDITION MUST FOLLOW MULTIPLICATION BY SCALE VALUE

    if tsn.shift is not None:
        const += tsn.shift.mu

    return np.array([const, coeff])


def ts_expected_polynomials(array: list[TriangleSymmetric[Normal]]) -> np.ndarray:
    return np.stack([expected_as_polynomial(fz) for fz in array]).T
