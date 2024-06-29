"""Triangle Symmetric Normal Distribution Shift Scale Representation"""

import numpy as np

from src.algebra import (
    solve_matrix,
    intersect_segments,
    apply_gt_constraints,
    apply_lt_constraints,
    rest_mask,
    is_float_less,
    frontier_derivation,
    lowest_parabola_point,
)
from src.common import number
from src.fuzzy import TriangleSymmetric
from src.probability import Normal


def _expected_as_polynomial(tsn: TriangleSymmetric[Normal]) -> np.ndarray:
    return np.array([tsn.mode.mu, tsn.diameter.mu / 2])


def tsn_expected_polynomials(array: list[TriangleSymmetric[Normal]]) -> np.ndarray:
    return np.stack([_expected_as_polynomial(fz) for fz in array]).T


def _dispersion(tsn: TriangleSymmetric[Normal]) -> number:
    return tsn.mode.sigma2 + tsn.diameter.sigma2 / 12


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


def efficient_portfolio_frontier_no_shorts(sysmatrix: np.ndarray):
    expected = sysmatrix[-2, :-2]
    qf = sysmatrix[:-2, :-2]
    size = len(expected)

    lowest = expected.argmin()
    highest = expected.argmax()

    idx = [lowest]
    result = []
    black_list = set(tuple(idx))
    dropped_shares = set()

    illbeback = False
    hard_limit = expected.min()

    while idx != [highest]:
        new_vals = None

        for can in set(range(size)) - set(idx):
            ix = sorted(idx + [can])
            if tuple(ix) in black_list:
                continue

            muted = sorted(set(range(size)) - set(ix))
            skip = {i: 0 for i in muted}
            poly = solve_frontier(sysmatrix, skip)

            mask = rest_mask(size, muted)

            (low, high), dropouts = intersect_segments(
                apply_gt_constraints(poly, np.zeros(size), mask),
                apply_lt_constraints(poly, np.ones(size), mask),
            )

            # check if solution is required short selling
            if low >= high:
                continue  # no short selling

            # check if solution attached before hard limit
            if is_float_less(low, hard_limit):
                continue  # not optimal solution

            if new_vals is None:
                left_border = low
                derivation = frontier_derivation(low, qf, poly)
                approved = can
                new_vals = {
                    "index": ix,
                    "segment": (low, high),
                    "dropouts": dropouts,
                    "poly": poly,
                    "point": lowest_parabola_point(qf, poly),
                }
                continue  # check next solution

            d = frontier_derivation(low, qf, poly)

            if is_float_less(low, left_border) or (
                np.isclose(low, left_border) and d < derivation
            ):
                left_border = low
                derivation = d
                approved = can
                new_vals = {
                    "index": ix,
                    "segment": (low, high),
                    "dropouts": dropouts,
                    "poly": poly,
                    "point": lowest_parabola_point(qf, poly),
                }

        if new_vals:
            hard_limit = new_vals["segment"][0]

            if result:
                result[-1]["segment"] = (
                    result[-1]["segment"][0],  # keep left
                    hard_limit,  # update right
                )

            illbeback = illbeback or (approved in dropped_shares)

            idx = new_vals["index"]
            black_list.add(tuple(idx))
            result.append(new_vals)
        else:
            assert len(idx) != 1, (
                "All assets dropped before maximum return is reached"
                + f"\n{sysmatrix=}\n{result=}"
            )

            hard_limit = result[-1]["segment"][1]
            drop = result[-1]["dropouts"][1]
            dropped_shares.add(drop)

            idx = sorted(set(idx) - {drop})
            black_list.add(tuple(idx))

            if len(idx) == 1:
                # singular point is reached
                # nothing to add
                continue

            muted = sorted(set(range(size)) - set(idx))
            skip = {i: 0 for i in muted}
            poly = solve_frontier(sysmatrix, skip)

            mask = rest_mask(size, muted)

            (_, high), dropouts = intersect_segments(
                apply_gt_constraints(poly, np.zeros(size), mask),
                apply_lt_constraints(poly, np.ones(size), mask),
            )

            new_vals = {
                "index": idx,
                "segment": (
                    hard_limit,  # update left point
                    high,  # keep right point
                ),
                "dropouts": dropouts,
                "poly": poly,
                "point": lowest_parabola_point(qf, poly),
            }

            result.append(new_vals)

    return result, illbeback
