import numpy as np
from matplotlib.axes import Axes
from scipy.stats import rv_continuous

from src.fuzzy import TriangleSymmetric, Measure
from src.lang import *
from src.probability import Normal


def _normalized(xs, dist: rv_continuous):
    v = dist.pdf(xs)
    return v / v.max()


def plot_schematic(ax: Axes, ssr: TriangleSymmetric[Normal], precision=256):
    mid = ssr.to_random(0)

    left = ssr.to_random(-1)
    right = ssr.to_random(1)

    xmin, xmax = left.mu - 2 * left.sigma2 ** 0.5, right.mu + 2 * right.sigma2 ** 0.5
    xs = np.linspace(xmin, xmax, precision)
    ys = np.linspace(0, 1, precision)
    source = np.meshgrid(xs, ys)

    pess = np.stack(
        [
            _normalized(xs, ssr.to_random(alpha, Measure.NECESSITY).to_scipy_stat())
            for alpha in ys
        ]
    )

    opt = np.stack(
        [
            _normalized(
                xs, ssr.to_random(1 - alpha, Measure.POSSIBILITY).to_scipy_stat()
            )
            for alpha in ys
        ]
    )

    background_level = 0.15
    contour_lines_level = 0.3

    # hack to expand y-limit
    ax.plot((xmin, xmax), (-0.01, 1.01), alpha=0)

    # background
    ax.contourf(
        *source,
        np.maximum(pess, opt),
        cmap="Greys",
        levels=(background_level, 1),
        antialiased=True,
        alpha=0.5,
    )

    # blue contour
    ax.contour(
        *source,
        pess,
        colors=("#5555ff",),
        linestyles="--",
        levels=(contour_lines_level, 1),
    )

    # fake line for label in legend
    ax.plot(
        [xmin, xmax],
        [1, 1],
        linestyle="--",
        c="#5555ff",
        label=K_PESSIMISTIC,
    )

    # red contour
    ax.contour(
        *source,
        opt,
        colors=("#ff5555",),
        linestyles="--",
        levels=(contour_lines_level, 1),
    )

    # fake line for label in legend
    ax.plot(
        [xmin, xmax],
        [1, 1],
        linestyle="--",
        c="#ff5555",
        label=K_OPTIMISTIC,
    )

    # median line
    ax.plot(
        [left.mu, mid.mu, right.mu],
        [0, 1, 0],
        linestyle=":",
        linewidth=2,
        c="k",
        label=K_EXPECTED,
    )
