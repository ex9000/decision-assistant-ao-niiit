import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde
from tqdm import tqdm

from src.algebra import (
    make_covariance,
    quadratic_form,
)
from src.tsn_ssr import compose_system

np.random.seed(25)

size = 3
expected = np.array(list(range(size)))
dispersion = np.array([5] * size)

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors**2).sum(axis=0))
correlation = vectors.T @ vectors

covariance = make_covariance(dispersion, correlation)
sysmatrix = compose_system(expected, covariance)

xmin = ymin = 10**100
xmax = ymax = -(10**100)
dots = []


for i in tqdm(range(10**4)):
    param = 3.8
    w = param ** (param * np.random.uniform(size=size))
    w /= w.sum()

    xpos = w @ expected
    ypos = quadratic_form(covariance, w[..., np.newaxis])
    xmin = min(xmin, xpos)
    xmax = max(xmax, xpos)
    ymin = min(ymin, ypos)
    ymax = max(ymax, ypos)
    dots.append([xpos, ypos[0]])

print(f"{len(dots)=}")
dots = np.array(dots).T


fig, ax = plt.subplots(1, figsize=(10, 8))

xs = np.linspace(min(expected) - 1, max(expected) + 1, 1000)

k = gaussian_kde(dots)
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
ax.pcolormesh(xi, yi, zi, shading="gouraud", zorder=-1, cmap="Blues")
ax.scatter(*dots[..., : 10**3], marker="x", zorder=5, color="k")

for sp in ax.spines.values():
    sp.set_visible(False)

ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

ax.scatter(expected, dispersion, marker="*", c="gold", s=300, zorder=50)


plt.show()
