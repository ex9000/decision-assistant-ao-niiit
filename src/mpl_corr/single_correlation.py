import numpy as np
from matplotlib.axes import Axes
from scipy.stats import gaussian_kde

from src.geometry import pol2cart


def plot_correlation(ax: Axes, correlation: float, amount=10 ** 4):
    correlation = np.clip(correlation, -0.95, 0.95)

    corr_mat = np.array([[1.0, correlation], [correlation, 1.0]])

    data = np.random.multivariate_normal([0, 0], corr_mat, amount).T

    k = gaussian_kde(data)
    val = np.percentile(abs(data), 96)
    xi, yi = np.meshgrid(*(2 * [np.linspace(-val, +val, 64)]))
    zi = k(np.vstack([xi.flatten(), yi.flatten()])).reshape(xi.shape)
    zi -= zi.min()
    zi /= zi.max()

    cs = ax.contour(xi, yi, zi, cmap="ocean")
    ax.clabel(cs, fontsize=14)


def plot_shooting_target(ax: Axes, correlation: float):
    xi, yi = np.meshgrid(*(2 * [np.linspace(-10, +10, 256)]))
    zi = 11 - (xi ** 2 + yi ** 2) ** 0.5

    # circles
    ax.contourf(
        xi,
        yi,
        zi,
        colors=["grey", "white"] * 5,
        levels=range(1, 11),
        antialiased=True,
    )

    # 10 scores at center
    style = dict(
        fontsize=15,
        color="black",
        fontweight="bold",
        horizontalalignment="center",
        verticalalignment="center",
    )
    ax.text(0, 0, "10", **style)

    # 1 to 9 scores
    style["fontsize"] = 12
    del style["color"]
    for i in range(1, 10):
        a, b = 10.45 - i, 0
        color = "black" if i % 2 == 0 else "white"
        for x, y in [(a, b), (-a, b)]:  # , (b, a), (b, -a)]:
            ax.text(x, y, str(i), color=color, **style)

    # inner/outer bounds of "hits"
    left, right = 0, 9.5
    if correlation > 0:
        right = 1 + (right - 1) * (1 - correlation)
    else:
        left = -correlation * (right - 1)

    # generate kinda uniform distribution of points
    lucky_amount = 50  # only one cross in at 10 scores
    gr = 1.618033988749894  # golden ratio distribution
    dist = (gr * 10 * np.arange(lucky_amount)) % 10
    dist -= dist.min()
    dist /= dist.max()
    dist = dist ** 0.5
    dist *= right - left
    dist += left

    # place dots on circle
    dots = pol2cart(np.linspace(0, 2 * np.pi, lucky_amount), dist)

    # fix "hits" markers size at very center
    # when correlation > threshold
    size = 80
    threshold = 0.4
    if correlation > threshold:
        minsize = 12
        size = minsize + (1 - correlation) * (size - minsize) / (1 - threshold)

    # draw markers
    ax.scatter(*dots, marker="X", color="red", s=size)
