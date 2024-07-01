import numpy as np
from matplotlib import cm as mpl_cm
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval
from scipy.stats import gaussian_kde
from tqdm import tqdm

from src.algebra import make_covariance, quadratic_form
from src.fuzzy import TriangleSymmetric
from src.lang import K_EXPECTED_VALUE, K_DISPERSION, switch_lang, Lang
from src.mpl_main.figparams import FigParams, final_patch, LegendType
from src.probability import Normal
from src.tsn_ssr import (
    tsn_dispersion,
    tsn_expected_polynomials,
    compose_system,
    efficient_portfolio_frontier_no_shorts,
)

size, seed = 10, 42
smooth = False

assets = [
    Normal(i, 0.1 * (i + 1)) + Normal(i + 1, i + 2) * TriangleSymmetric(0.1 * i, 1)
    for i in range(1, 2 * size, 2)
]

expected = polyval(0.5, tsn_expected_polynomials(assets))
dispersion = tsn_dispersion(assets).round(2)


np.random.seed(seed)

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors**2).sum(axis=0))

corr = vectors.T @ vectors
corr = corr.round(2)

covariance = make_covariance(dispersion, corr)
system = compose_system(expected, covariance)

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


print(f"{expected=}")
print(f"{dispersion=}")


xmin = ymin = 10**100
xmax = ymax = -(10**100)

dots = []
weights = dict()
for i in tqdm(range(10**5)):
    param = 10
    w = param ** (param * np.random.uniform(size=size))
    w /= w.sum()

    xpos = w @ expected
    ypos = quadratic_form(covariance, w[..., np.newaxis])
    weights[(xpos, ypos[0])] = w
    xmin = min(xmin, xpos)
    xmax = max(xmax, xpos)
    ymin = min(ymin, ypos)
    ymax = max(ymax, ypos)
    dots.append([xpos, ypos[0]])

print(f"{len(dots)=}")
adots = np.array(dots[: 10**4]).T

switch_lang(Lang.RU)
fig, ax = FigParams((10, 6)).init_ax_fig()

d = max(expected) - min(expected)
xs = np.linspace(min(expected) - 0.1 * d, max(expected) + 0.1 * d, 1000)


if smooth:
    k = gaussian_kde(adots)
    dx = xmax - xmin
    dy = ymax - ymin
    xi, yi = np.meshgrid(
        np.linspace(xmin - 0.1 * dx, xmax + 0.1 * dx, 128),
        np.linspace(ymin - 0.1 * dy, ymax + 0.1 * dy, 128),
    )
    zi = k(np.vstack([xi.flatten(), yi.flatten()])).reshape(xi.shape)
    zi -= zi.min()
    zi /= zi.max()
    # ax.contourf(xi, yi, zi, zorder=-2)
    ax.pcolormesh(xi, yi, zi, shading="gouraud", zorder=-10, cmap="Blues")

ax.scatter(*adots[..., : 10**3], marker="x", zorder=0, color="k")

for txt, x, y in zip(names, expected, dispersion):
    ax.annotate(txt.title(), (x, y), zorder=100, ha="right")


ax.scatter(expected, dispersion, marker="*", c="gold", s=300, zorder=50)

# FIND BORDER
rdots = sorted(dots[:300], reverse=True)

border = [rdots[0]]
for p in rdots:
    if p[1] < border[-1][1]:
        border.append(p)

ax.scatter(*list(zip(*border)), marker="x", zorder=3, color="k")
ax.plot(*list(zip(*border)), marker="o", zorder=2, color="crimson", label="300 Точек")

# FIND ABSOLUTE BORDER
gdots = sorted(dots, reverse=True)

border = [tuple(gdots[0])]
for p in gdots:
    if p[1] < border[-1][1]:
        border.append(tuple(p))

ax.scatter(*list(zip(*border)), marker="x", zorder=5, color="k")
ax.plot(
    *list(zip(*border)), marker="o", zorder=4, color="limegreen", label="10^5 Точек"
)


# GROUND TRUTH
labeled = False
result, _ = efficient_portfolio_frontier_no_shorts(system)
for r in result:
    sol = r.poly
    (left, right) = r.segment
    if r.point[0] > r.right:
        continue

    rest = xs[(xs > left) & (xs < right)]
    w = polyval(rest, sol)
    ys = quadratic_form(covariance, w)

    if not labeled:
        ax.plot(rest, ys, c="royalblue", linewidth=3, zorder=0, label="Авторский Метод")
        labeled = True
    else:
        ax.plot(rest, ys, c="royalblue", linewidth=3, zorder=0)

if not smooth:
    hy = max(dispersion)
    has_label = set()
    dcolors = np.array(mpl_cm.tab10.colors)
    dcolors = dcolors ** np.full(dcolors.shape, 0.2)
    dcolors = dict(zip(range(size), dcolors))

    for p1, p2 in zip(border, border[1:]):
        x1, y1 = p1
        x2, y2 = p2

        w1 = weights[p1]
        w2 = weights[p2]
        vals = np.stack([w1, w2])
        vals = np.concatenate([np.zeros((2, 1)), vals], axis=1)
        vals = vals.cumsum(axis=1) * hy

        outline = False
        for i in range(size):
            args = ([x1, x2], vals[..., i], vals[..., i + 1])
            if i != size - 1:
                ax.plot(args[0], args[2], c="black", linestyle="--", lw=0.7, zorder=-4)
            outline = True
            if i not in has_label:
                has_label.add(i)
                ax.fill_between(
                    *args,
                    color=dcolors[i % len(dcolors)],
                    label=names[i] if i < len(names) else f"{i=}",
                    zorder=-5,
                )
            else:
                ax.fill_between(*args, color=dcolors[i % len(dcolors)], zorder=-5)

final_patch(
    ax,
    legend=LegendType.LOC,
    ax_labels=(K_EXPECTED_VALUE.title(), K_DISPERSION.title()),
)

plt.show()
plt.close(fig)
