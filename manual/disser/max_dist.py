import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm, rv_continuous

np.random.seed(44)


fig, ax = plt.subplots(1, figsize=(10, 8))

xs = np.linspace(0, 10, 1000)

n1: rv_continuous = norm(3, 1)
n2: rv_continuous = norm(4, 2)

ax.plot(
    xs,
    n1.pdf(xs),
    label="Нормальные величины",
    color="royalblue",
    linestyle=":",
    linewidth=2,
)
ax.plot(xs, n2.pdf(xs), color="royalblue", linestyle=":", linewidth=2)

ys = np.diff(n1.cdf(xs) * n2.cdf(xs))
mean = (xs[:-1] * ys).sum()
var = ((xs[:-1] - mean) ** 2 * ys).sum()
approx = norm(mean, var**0.5)
ax.plot(
    xs,
    approx.pdf(xs),
    label="Аппроксимация нормальным распределением",
    color="crimson",
    linewidth=3,
)

pys = ys / ys.sum() / (xs[1] - xs[0])
ax.plot(xs[:-1], pys, label="Максимум величин", color="limegreen", linewidth=3)

ax.grid()
ax.legend(loc="best")

ax.set_xticklabels([])
ax.set_yticklabels([])

plt.show()
