from itertools import combinations, chain

import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval

from src.algebra import (
    make_covariance,
    apply_gt_constraints,
    apply_lt_constraints,
    intersect_segments,
    quadratic_form,
)
from src.tsn_ssr import compose_system, solve_frontier

np.random.seed(44)

expected = np.array(list(range(3)))
dispersion = np.array([5] * len(expected))
assert len(expected) == len(dispersion)
size = len(expected)

correlation = np.eye(size)


subsets = list(chain(*map(lambda i: combinations(range(size), i), range(size - 1))))
covariance = make_covariance(dispersion, correlation)
sysmatrix = compose_system(expected, covariance)


sol = solve_frontier(sysmatrix)
(left, right), *_ = intersect_segments(
    apply_gt_constraints(sol, np.zeros(size)),
    apply_lt_constraints(sol, np.ones(size)),
)

fig, ax = plt.subplots(1, figsize=(10, 8))

d = max(expected) - min(expected)
xs = np.linspace(min(expected) - 0.1 * d, max(expected) + 0.1 * d, 1000)

for sp in ax.spines.values():
    sp.set_visible(False)

ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

ax.scatter(expected, dispersion, marker="*", c="gold", s=300, zorder=50)

rest = xs  # [(xs > left) & (xs < right)]
weights = polyval(rest, sol)
ax.plot(rest, quadratic_form(covariance, weights), c="k", linewidth=5)

rest = xs[(xs > left) & (xs < right)]
weights = polyval(rest, sol)
ax.plot(rest, quadratic_form(covariance, weights), c="lime", linewidth=3)

plt.show()
