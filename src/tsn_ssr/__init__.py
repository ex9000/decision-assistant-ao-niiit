"""Triangle Symmetric Normal Distribution Shift Scale Representation"""

from dataclasses import dataclass

import numpy as np

from src.algebra import (
    solve_matrix,
    apply_gt_constraints,
    rest_mask,
    is_float_less,
    frontier_derivation,
    lowest_parabola_point,
    is_float_lequal,
)
from src.common import number
from src.fuzzy import TriangleSymmetric
from src.probability import Normal


@dataclass
class SolutionPart:
    index: tuple[int]
    segment: tuple[float, float]
    dropouts: tuple[int, int]
    poly: np.ndarray
    point: tuple[float, float]

    @property
    def left(self) -> float:
        return self.segment[0]

    @property
    def right(self) -> float:
        return self.segment[1]

    @property
    def left_id(self) -> int:
        return self.dropouts[0]

    @property
    def right_id(self) -> int:
        return self.dropouts[1]

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)


def _expected_as_polynomial(tsn: TriangleSymmetric[Normal]) -> np.ndarray:
    return np.array(
        [tsn.shift.mu + tsn.scale.mu * tsn.mode, 0.5 * tsn.scale.mu * tsn.diameter]
    )


def tsn_expected_polynomials(array: list[TriangleSymmetric[Normal]]) -> np.ndarray:
    return np.stack([_expected_as_polynomial(fz) for fz in array]).T


def _dispersion(tsn: TriangleSymmetric[Normal]) -> number:
    return tsn.shift.sigma2 + tsn.scale.sigma2 * (tsn.mode**2 + tsn.diameter**2 / 12)


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


def efficient_portfolio_frontier_no_shorts(
    sysmatrix: np.ndarray,
) -> tuple[list[SolutionPart], bool]:
    expected = sysmatrix[-2, :-2]
    qf = sysmatrix[:-2, :-2]
    size = len(expected)

    lowest: int = int(expected.argmin())
    highest: int = int(expected.argmax())

    idx = (lowest,)
    result = []
    black_list = set(tuple(idx))
    dropped_shares = set()

    illbeback = False
    hard_limit = expected.min()

    while idx != (highest,):
        new_vals: SolutionPart | None = None

        for can in set(range(size)) - set(idx):
            # noinspection PyTypeChecker
            ix: tuple[int] = tuple(sorted(list(idx) + [can]))

            if ix in black_list:
                continue

            muted: list[int] = sorted(set(range(size)) - set(ix))
            skip = {i: 0 for i in muted}
            poly = solve_frontier(sysmatrix, skip)

            mask = rest_mask(size, muted)

            (low, high), dropouts = apply_gt_constraints(poly, np.zeros(size), mask)

            # check if solution is required short selling
            if is_float_lequal(high, low):
                continue  # no short selling

            # check if solution attached before hard limit
            if is_float_less(low, hard_limit):
                continue  # not optimal solution

            if result and is_float_less(result[-1]["segment"][1], low):
                continue  # disjoint with last segment

            if new_vals is None:
                left_border = low
                derivation, second = frontier_derivation(low, qf, poly)
                approved = can
                new_vals = SolutionPart(
                    index=tuple(ix),
                    segment=(low, high),
                    dropouts=dropouts,
                    poly=poly,
                    point=lowest_parabola_point(qf, poly),
                )
                continue  # check next solution

            d, dd = frontier_derivation(low, qf, poly)

            if is_float_less(left_border, low):
                continue

            if np.isclose(low, left_border):
                if is_float_less(derivation, d):
                    continue
                if d > 0 == is_float_less(second, dd):
                    continue

            left_border = low
            second = dd
            derivation = d
            approved = can
            new_vals = SolutionPart(
                index=ix,
                segment=(low, high),
                dropouts=dropouts,
                poly=poly,
                point=lowest_parabola_point(qf, poly),
            )

        if new_vals:
            hard_limit = new_vals["segment"][0]

            if result:
                result[-1]["segment"] = (
                    result[-1]["segment"][0],  # keep left
                    hard_limit,  # update right
                )

            illbeback = illbeback or (approved in dropped_shares)

            idx = new_vals["index"]
            black_list.add(idx)
        else:
            assert len(idx) != 1, (
                "All assets dropped before maximum return is reached"
                + f"\n{expected=}\n{lowest=}\n{highest=}\n{sysmatrix=}\n{result=}"
            )

            hard_limit = result[-1]["segment"][1]
            drop = result[-1]["dropouts"][1]
            dropped_shares.add(drop)

            # noinspection PyTypeChecker
            idx: tuple[int] = tuple(sorted(set(idx) - {drop}))
            black_list.add(tuple(idx))

            if len(idx) == 1:
                # singular point is reached
                # nothing to add
                continue

            muted = sorted(set(range(size)) - set(idx))
            skip = {i: 0 for i in muted}
            poly = solve_frontier(sysmatrix, skip)

            mask = rest_mask(size, muted)

            (_, high), dropouts = apply_gt_constraints(poly, np.zeros(size), mask)

            new_vals = SolutionPart(
                index=idx,
                segment=(
                    hard_limit,  # update left point
                    high,  # keep right point
                ),
                dropouts=dropouts,
                poly=poly,
                point=lowest_parabola_point(qf, poly),
            )

        assert new_vals is not None
        result.append(new_vals)

    return result, illbeback
