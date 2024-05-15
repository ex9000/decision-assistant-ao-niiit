from itertools import combinations, chain, product

import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval
from scipy.stats import gaussian_kde
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

np.random.seed(44)

expected = np.array([1, 2, 3, 4, 0])
dispersion = np.array([10, 1, 7, 8, 2])
correlation = np.eye(5) + (1 - np.eye(5)) * np.random.uniform(-1, 1, size=(5, 5))
correlation = 0.5 * (correlation + correlation.T)
# correlation[-1, :] = correlation[:, -1] = np.ones(5)

minimal, maximal = 0.2, 1  # 0.5

ground_truth = False
if ground_truth:
    size = 4
    subsets = list(chain(*map(lambda i: combinations(range(4), i), range(3))))
    covariance = make_covariance(dispersion[:-1], correlation[:-1, :-1])
    sysmatrix = compose_system(expected[:-1], covariance)

    lower = np.full(size, minimal)
    upper = np.full(size, maximal)
else:
    size = 5
    subsets = list(chain(*map(lambda i: combinations(range(5), i), range(4))))
    covariance = make_covariance(dispersion, correlation)
    sysmatrix = compose_system(expected, covariance)

    lower = np.full(size, minimal)
    upper = np.full(size, maximal)

    # lower[-1] = 0
    # upper[-1] = 1

xmin = ymin = 10 ** 100
xmax = ymax = -(10 ** 100)
dots = []
for i in tqdm(range(10 ** 5)):
    w = 5 ** (5 * np.random.uniform(size=size))
    for i in range(size):
        if w.sum() == 0:
            break
        w /= w.sum()
        if np.any((w < minimal) & (w > 0)):
            w[w < minimal] = 0
            continue
        xpos = w @ expected
        ypos = quadratic_form(covariance, w[..., np.newaxis])
        xmin = min(xmin, xpos)
        xmax = max(xmax, xpos)
        ymin = min(ymin, ypos)
        ymax = max(ymax, ypos)
        dots.append([xpos, ypos[0]])

        w[w == (w[w > 0].min())] = 0
dots = np.array(dots).T

free = []
for grp in tqdm(subsets):
    mask = rest_mask(size, list(grp))
    sol = solve_frontier(sysmatrix, {i: 0 for i in grp})
    (left, right), *_ = intersect_segments(
        apply_gt_constraints(sol, np.zeros(size), mask),
        apply_lt_constraints(sol, np.ones(size), mask),
    )

    free.append((left, right, sol))

limited = []
# for grp in tqdm(subsets):
#     mask = rest_mask(4, list(grp))
#     sol = solve_frontier(sysmatrix, {i: 0 for i in grp})
#     (left, right), *_ = intersect_segments(
#         apply_gt_constraints(sol, np.full(4, minimal), mask),
#         apply_lt_constraints(sol, np.full(4, maximal), mask),
#     )
#
#     limited.append((left, right, sol))

fixed = []
intermediate = []
for grp in tqdm(subsets):
    mask = rest_mask(size, list(grp))
    for limits in product([0, minimal, maximal], repeat=len(grp)):
        sol = solve_frontier(sysmatrix, dict(zip(grp, limits)))
        (left, right), *_ = intersect_segments(
            apply_gt_constraints(sol, lower, mask),
            apply_lt_constraints(sol, upper, mask),
        )

        if sum(limits) == 0:
            limited.append((left, right, sol))
        elif 0 in limits:
            intermediate.append((left, right, sol))
        else:
            fixed.append((left, right, sol))

fig, ax = plt.subplots(1, figsize=(10, 8))

xs = np.linspace(min(expected), max(expected), 1000)

k = gaussian_kde(dots)
xi, yi = np.meshgrid(np.linspace(xmin, xmax, 64), np.linspace(ymin, ymax, 64))
zi = k(np.vstack([xi.flatten(), yi.flatten()])).reshape(xi.shape)
zi -= zi.min()
zi /= zi.max()
# ax.contourf(xi, yi, zi, zorder=-2)
ax.scatter(*dots, marker="d", zorder=-5)

ax.scatter(expected, dispersion, zorder=50)
for xmin, xmax, sol in free:
    rest = xs[(xs > xmin) & (xs < xmax)]
    if len(rest) < 2:
        continue

    weights = polyval(rest, sol)
    ax.plot(rest, quadratic_form(covariance, weights), c="k", linewidth=4)

    x, y = lowest_parabola_point(covariance, sol)
    if xmin < x < xmax:
        ax.scatter(x, y, marker="*", c="gold", s=100, zorder=100)

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

for xmin, xmax, sol in intermediate:
    rest = xs[(xs > xmin) & (xs < xmax)]
    if len(rest) < 2:
        continue

    weights = polyval(rest, sol)
    ax.plot(
        rest, quadratic_form(covariance, weights), c="tomato", linewidth=2, zorder=40
    )

plt.show()
