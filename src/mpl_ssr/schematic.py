import numpy as np
from matplotlib.axes import Axes
from scipy.stats import rv_continuous

from src.fuzzy import TriangleSymmetric, Measure
from src.lang import *
from src.mpl_ssr.plotting import prepare_plot
from src.probability import Normal


def _normalized(xs, dist: rv_continuous):
    v = dist.pdf(xs)
    return v / v.max()


def plot_schematic(ax: Axes, ssr: TriangleSymmetric[Normal], precision=256):
    left, right, source, xmax, xmin, xs, ys = prepare_plot(ax, precision, ssr)

    mid = ssr.to_random(0)

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
