import numpy as np
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval

from src.algebra import (
    make_covariance,
    apply_gt_constraints,
    quadratic_form,
)
from src.lang import *
from src.mpl_main import NORMAL_FIG_PARAMS, final_patch, LegendType
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

perm = [x - 1 for x in [3, 2, 5, 1, 4]]
# perm = [x - 1 for x in [2, 1, 5, 3, 4]]
expected = expected[perm]
dispersion = dispersion[perm]
vectors = vectors[..., perm]
expected = expected.round(0)
dispersion = dispersion.round(0)

# corr = np.eye(size)
corr = vectors.T @ vectors
corr = corr.round(1)

covariance = make_covariance(dispersion, corr)

system = compose_system(expected, covariance)

result, _ = efficient_portfolio_frontier_no_shorts(system)
print(result)

switch_lang(Lang.RU)

fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

names = [
    "Анна",
    "Борис",
    "Василий",
    "Григорий",
    "Дмитрий",
    "Елена",
    "Женя",
    "Зинаида",
    "Иван",
    "Константин",
    "Леонид",
    "Михаил",
    "Николай",
    "Ольга",
    "Павел",
    "Роман",
    "Семён",
    "Татьяна",
    "Ульяна",
    "Фёдор",
    "Харитон",
    "Шура",
    "Юрий",
    "Яков",
]


xs = np.linspace(result[0]["segment"][0], result[-1]["segment"][1], 1000)

step_index = 6
if step_index == 0:
    curr_ix = {np.argmin(expected)}
else:
    curr_ix = set(result[step_index - 1]["index"])

for i in range(step_index - 1):
    sol = result[i]["poly"]
    left, right = result[i]["segment"]
    rest = xs[(xs > left) & (xs < right)]
    weights = polyval(rest, sol)
    ys = quadratic_form(covariance, weights)
    ax.plot(rest, ys, c="k", linewidth=3, linestyle=":", zorder=-2)

if step_index > 0:
    sol = solve_frontier(system, {j: 0 for j in range(size) if j not in curr_ix})
    (left, right), *_ = apply_gt_constraints(sol, np.zeros(size))

    rest = xs[(xs > left) & (xs < right)]
    weights = polyval(rest, sol)
    ys = quadratic_form(covariance, weights)
    name = " ".join(names[j] for j in curr_ix)
    ax.plot(rest, ys, c="k", linewidth=3, zorder=-2, label=name.title())

has_green = False
for i in range(size):
    if i in curr_ix:
        continue
    step_ix = curr_ix | {i}
    sol = solve_frontier(system, {j: 0 for j in range(size) if j not in step_ix})
    (left, right), *_ = apply_gt_constraints(sol, np.zeros(size))

    rest = xs[(xs > left) & (xs < right)]
    weights = polyval(rest, sol)
    ys = quadratic_form(covariance, weights)

    if step_ix == set(result[step_index]["index"]):
        has_green = True
        name = " ".join(names[j] for j in step_ix)
        ax.plot(rest, ys, c="limegreen", linewidth=3, zorder=0, label=name.title())
    else:
        ax.plot(rest, ys, c="crimson", linewidth=3, zorder=-1)

if not has_green:
    step_ix = curr_ix - {result[step_index - 1]["dropouts"][1]}

    sol = solve_frontier(system, {j: 0 for j in range(size) if j not in step_ix})
    (left, right), *_ = apply_gt_constraints(sol, np.zeros(size))

    rest = xs[(xs > left) & (xs < right)]
    weights = polyval(rest, sol)
    ys = quadratic_form(covariance, weights)
    name = " ".join(names[j] for j in step_ix)

    ax.plot(rest, ys, c="royalblue", linewidth=3, zorder=-3, label=name.title())

ax.scatter(expected, dispersion, marker="*", c="gold", s=300, zorder=50)

for txt, x, y in zip(names, expected, dispersion):
    ax.annotate(txt.title(), (x, y), zorder=100)

final_patch(
    ax,
    legend=LegendType.LOC,
    ax_labels=(K_EXPECTED_VALUE.title(), K_DISPERSION.title()),
)

ax.set_xticklabels([])
ax.set_xticks([])
ax.set_yticklabels([])
ax.set_yticks([])

ax.set_xlim(xs[0] - 1, xs[-1] + 1)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()

plt.show()
plt.close(fig)
