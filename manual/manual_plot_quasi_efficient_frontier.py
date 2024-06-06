import matplotlib.cm as mpl_cm
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval

from src.algebra import make_covariance, quadratic_form
from src.tsn_ssr import compose_system, efficient_portfolio_frontier_no_shorts

size = 10
np.random.seed(49)

expected = np.random.randint(1, 15, size=size) + np.random.random(size) * 0.1
dispersion = np.random.randint(1, 15, size=size) + np.random.random(size) * 0.1

assert len(set(zip(dispersion, expected))) == size

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors ** 2).sum(axis=0))
corr = vectors.T @ vectors

covariance = make_covariance(dispersion, corr)

system = compose_system(expected, covariance)

result, _ = efficient_portfolio_frontier_no_shorts(system)
print(result)

V = expected
M = covariance
data = pd.DataFrame(result).to_dict(orient="list")

lx, hx = min(V), max(V)
xx = hx - lx
lx -= 0.15 * xx
hx += 0.15 * xx

ly, hy = 0, np.diag(M).max()
yy = hy - ly
hy += 0.10 * yy

xs = np.linspace(lx, hx, 1000)

fig, ax = plt.subplots(1, figsize=(10, 8))
ax.set_title("Frontier with shares")
ax.grid(True)

indices = range(size)
names = list(map(str, range(size)))

dcolors = np.array(mpl_cm.tab10.colors)
dcolors = dcolors ** np.full(dcolors.shape, 0.2)
dcolors = dict(zip(indices, dcolors))

ax.scatter(V, np.diag(M), c="black", zorder=100)
for txt, x, y in zip(names, V, np.diag(M)):
    ax.annotate(txt.title(), (x, y), zorder=100)

labeled = {i: False for i in indices}
for idx, poly, (mn, mx), (x, y) in zip(
        data["index"], data["poly"], data["segment"], data["point"]
):

    ws = polyval(xs, poly)
    ys = quadratic_form(M, ws)

    if mn <= x <= mx:
        ax.axvline(x=x, c="black", linestyle="--")

    has_label = [i for i in idx if not labeled[i]]
    for i in idx:
        labeled[i] = True

    dotted = (mn <= xs) & (xs <= mx) & (xs <= x)
    solid = (mn <= xs) & (xs <= mx) & (xs >= x)

    if np.any(dotted):
        ax.plot(xs[dotted], ys[dotted], color="black", linestyle=":")

    if np.any(solid):
        ax.plot(xs[solid], ys[solid], color="black")

    ax.axvline(x=mn, lw=0.7, c="red", linestyle="--")
    ax.axvline(x=mx, lw=0.7, c="red", linestyle="--")

    vals = polyval(np.array([mn, mx]), poly).T
    vals = np.concatenate([np.zeros((2, 1)), vals], axis=1)
    vals = vals.cumsum(axis=1) * hy * 0.90

    outline = False
    for i in reversed(idx):
        args = ([mn, mx], vals[..., i], vals[..., i + 1])
        if outline:
            ax.plot(args[0], args[2], c="black", linestyle="--", lw=0.7, zorder=5)
        outline = True
        if i in has_label:
            ax.fill_between(*args, color=dcolors[i], label=names[i])
        else:
            ax.fill_between(*args, color=dcolors[i])

ax.legend()

plt.show()
