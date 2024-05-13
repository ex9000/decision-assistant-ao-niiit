from itertools import combinations, chain

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

covariance = make_covariance(dispersion, correlation)
sysmatrix = compose_system(expected, covariance)

minimal, maximal = 0.3, 0.4

subsets = chain(*map(lambda i: combinations(range(4), i), range(3)))

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

fig, ax = plt.subplots(1, figsize=(10, 10))

xs = np.linspace(min(expected), max(expected), 1000)

ax.scatter(expected, dispersion)
for xmin, xmax, sol in free:
    rest = xs[(xs > xmin) & (xs < xmax)]
    if len(rest) < 2:
        continue

    weights = polyval(rest, sol)
    ax.plot(rest, quadratic_form(covariance, weights), c="k", linewidth=2)

    x, y = lowest_parabola_point(covariance, sol)
    if xmin < x < xmax:
        ax.scatter(x, y, marker="*", c="y", s=100, zorder=100)

plt.show()
