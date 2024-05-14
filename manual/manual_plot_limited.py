from itertools import combinations, chain, product

import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval
from tqdm import tqdm

from src.algebra import (
    make_covariance,
    apply_gt_constraints,
    apply_lt_constraints,
    rest_mask,
    intersect_segments,
    quadratic_form,
    lowest_parabola_point,
)
from src.tsn_ssr import compose_system, solve_frontier

expected = np.array([1, 2, 3, 4, 0])
dispersion = np.array([10, 1, 7, 8, 12])
correlation = np.eye(5)
correlation[-1, :] = correlation[:, -1] = np.ones(5)

minimal, maximal = 0.1, 0.57

subsets = list(chain(*map(lambda i: combinations(range(4), i), range(3))))

covariance = make_covariance(dispersion[:-1], correlation[:-1, :-1])
sysmatrix = compose_system(expected[:-1], covariance)
free = []
for grp in tqdm(subsets):
    mask = rest_mask(4, list(grp))
    sol = solve_frontier(sysmatrix, {i: 0 for i in grp})
    (left, right), *_ = intersect_segments(
        apply_gt_constraints(sol, np.zeros(4), mask),
        apply_lt_constraints(sol, np.ones(4), mask),
    )

    free.append((left, right, sol))

limited = []
for grp in tqdm(subsets):
    mask = rest_mask(4, list(grp))
    sol = solve_frontier(sysmatrix, {i: 0 for i in grp})
    (left, right), *_ = intersect_segments(
        apply_gt_constraints(sol, np.full(4, minimal), mask),
        apply_lt_constraints(sol, np.full(4, maximal), mask),
    )

    limited.append((left, right, sol))

fixed = []
for grp in tqdm(subsets):
    mask = rest_mask(4, list(grp))
    for limits in product([minimal, maximal], repeat=len(grp)):
        sol = solve_frontier(sysmatrix, dict(zip(grp, limits)))
        (left, right), *_ = intersect_segments(
            apply_gt_constraints(sol, np.full(4, minimal), mask),
            apply_lt_constraints(sol, np.full(4, maximal), mask),
        )

        fixed.append((left, right, sol))

fig, ax = plt.subplots(1, figsize=(10, 8))

xs = np.linspace(min(expected), max(expected), 1000)

ax.scatter(expected, dispersion, zorder=50)
for xmin, xmax, sol in free:
    rest = xs[(xs > xmin) & (xs < xmax)]
    if len(rest) < 2:
        continue

    weights = polyval(rest, sol)
    ax.plot(rest, quadratic_form(covariance, weights), c="k", linewidth=4)

    x, y = lowest_parabola_point(covariance, sol)
    if xmin < x < xmax:
        ax.scatter(x, y, marker="*", c="y", s=100, zorder=100)

for xmin, xmax, sol in limited:
    rest = xs[(xs > xmin) & (xs < xmax)]
    if len(rest) < 2:
        continue

    weights = polyval(rest, sol)
    ax.plot(rest, quadratic_form(covariance, weights), c="lime", linewidth=3, zorder=25)

for xmin, xmax, sol in fixed:
    rest = xs[(xs > xmin) & (xs < xmax)]
    if len(rest) < 2:
        continue

    weights = polyval(rest, sol)
    ax.plot(
        rest, quadratic_form(covariance, weights), c="royalblue", linewidth=3, zorder=35
    )

plt.show()
