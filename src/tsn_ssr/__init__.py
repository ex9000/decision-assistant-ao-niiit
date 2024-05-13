"""Triangle Symmetric Normal Distribution Shift Scale Representation"""

import numpy as np

from src.algebra import solve_matrix
from src.fuzzy import TriangleSymmetric
from src.probability import Normal


def _expected_as_polynomial(tsn: TriangleSymmetric[Normal]) -> np.ndarray:
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


def tsn_expected_polynomials(array: list[TriangleSymmetric[Normal]]) -> np.ndarray:
    return np.stack([_expected_as_polynomial(fz) for fz in array]).T


def _dispersion(tsn: TriangleSymmetric[Normal]) -> np.ndarray:
    disp = tsn.mode + 1 / 12

    if tsn.scale is not None:
        disp *= tsn.scale.sigma2

    # DO NOT MOVE ANYTHING ABOVE THIS LINE
    # ADDITION MUST FOLLOW MULTIPLICATION BY SCALE VALUE

    if tsn.shift is not None:
        disp += tsn.shift.sigma2

    return disp


def tsn_dispersion(array: list[TriangleSymmetric[Normal]]) -> np.ndarray:
    return np.array([_dispersion(fz) for fz in array])


def compose_system(expected: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    assert expected.ndim == 1
    assert covariance.ndim == 2

    n = len(expected)
    assert (n, n) == covariance.shape

    result = np.ones((n + 2, n + 2))
    result[:n, :n] = 2 * covariance
    result[:n, n] = result[n, :n] = expected
    result[-2:, -2:] = 0

    return result


def solve_frontier(
        sysmatrix: np.ndarray,
        fixed: dict[int, float] = None,
        sum_constraint: float = 1,
) -> ((float, float), (int, int)):
    """Gets polynomial for a frontier"""

    assert sysmatrix.ndim == 2
    h, w = sysmatrix

    assert h == w

    mask = np.ones(h, dtype=bool)
    constants = np.array([])
    if fixed is not None:
        excluded = np.array(list(fixed))
        assert np.all(excluded[:-1] <= excluded[1:])

        mask[excluded] = False
        constants = np.array(list(fixed.values()))

    subsolution = solve_matrix(sysmatrix[mask][mask], sum_constraint - constants.sum())

    result = np.zeros((2, h))
    result[..., mask] = subsolution
    result[0, ~mask] = constants

    return result
