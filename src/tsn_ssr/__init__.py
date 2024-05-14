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
) -> np.ndarray:
    """Gets polynomial for a frontier"""

    assert sysmatrix.ndim == 2
    h, w = sysmatrix.shape

    assert h == w

    offset = np.zeros(h)
    offset[-1] = sum_constraint

    mask = np.ones(h, dtype=bool)
    constants = np.array([])
    if fixed is not None and fixed:
        # get array of indices
        excluded = np.array(list(fixed))
        assert np.all(excluded[:-1] <= excluded[1:])

        # fulfill the mask
        mask[excluded] = False
        constants = np.array(list(fixed.values()))

        # patch matrix and offset
        fixed_weights = np.zeros(h - 2)
        fixed_weights[~mask[:-2]] = constants

        ## !!
        patch = sysmatrix[:-2, :-2] @ fixed_weights
        patch[~mask[:-2]] = 0
        offset[:-2] -= patch  # some how

        offset[-2] -= sysmatrix[-2, :-2] @ fixed_weights
        offset[-1] -= fixed_weights.sum()

    subsolution = solve_matrix(
        sysmatrix[mask, ...][..., mask],
        offset[mask],
    )

    mask = mask[:-2]
    result = np.zeros((2, h - 2))
    result[..., mask] = subsolution
    result[0, ~mask] = constants

    return result
