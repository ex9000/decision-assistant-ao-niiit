import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval
from tqdm import tqdm

from src.algebra import (
    make_covariance,
    rest_mask,
    apply_gt_constraints,
    quadratic_form,
)
from src.common import subsets
from src.lang import *
from src.mpl_main import NORMAL_FIG_PARAMS, final_patch, LegendType, fig2pil
from src.mpl_shares import plot_shares_frontier
from src.tsn_ssr import (
    compose_system,
    efficient_portfolio_frontier_no_shorts,
    solve_frontier,
)

# (5, 15, 44) (5, 15, 43 back)
size, rng, seed = 5, 15, 42
np.random.seed(seed)

expected = np.random.randint(1, rng, size=size) + np.random.random(size) * 0.1
dispersion = np.random.randint(1, rng, size=size) + np.random.random(size) * 0.1

assert len(set(zip(dispersion, expected))) == size

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors**2).sum(axis=0))

# perm = [x - 1 for x in [3, 2, 5, 1, 4]]
# perm = [x - 1 for x in [2, 1, 5, 3, 4]]
# expected = expected[perm]
# dispersion = dispersion[perm]
# vectors = vectors[..., perm]

# corr = np.eye(size)
corr = vectors.T @ vectors

covariance = make_covariance(dispersion, corr)

system = compose_system(expected, covariance)

result, _ = efficient_portfolio_frontier_no_shorts(system)
print(result)

switch_lang(Lang.RU)

fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
plot_shares_frontier(ax, expected, covariance, names, result)

xs = np.linspace(result[0]["segment"][0], result[-1]["segment"][1], 1000)

plot_lines = False
if plot_lines:
    for grp in tqdm(list(subsets(size, biggest=size - 2))):
        mask = rest_mask(size, list(grp))
        sol = solve_frontier(system, {i: 0 for i in grp})
        (left, right), *_ = apply_gt_constraints(sol, np.zeros(size), mask)

        rest = xs[(xs > left) & (xs < right)]
        weights = polyval(rest, sol)
        ax.plot(rest, quadratic_form(covariance, weights), c="k", linewidth=0.2)


final_patch(
    ax,
    legend=LegendType.OUTSIDE,
    ax_labels=(K_EXPECTED_VALUE.title(), K_DISPERSION.title()),
)

ax.set_xticklabels([])
ax.set_xticks([])
ax.set_yticklabels([])
ax.set_yticks([])

im = fig2pil(fig)

im.show()

plt.show()
plt.close(fig)
ax.clear()
fig.clear()
del fig, ax
