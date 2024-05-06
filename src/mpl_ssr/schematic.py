import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Polygon

from src.fuzzy import TriangleSymmetric
from src.lang import *
from src.probability import Normal


def plot_schematic(ax: Axes, ssr: TriangleSymmetric[Normal]):
    left = ssr.to_random(-1)
    mid = ssr.to_random(0)
    right = ssr.to_random(1)

    l, p, r = left.mu, mid.mu, right.mu
    u, lu, ru = 3 * np.sqrt([mid.sigma2, left.sigma2, right.sigma2])

    y1 = np.array([[p - l - lu, 0], [p - l + lu, 0], [p + u, 1], [p - u, 1]])
    lp = Polygon(y1, facecolor="#aaffcc")
    y2 = np.array([[p + r - ru, 0], [p + r + ru, 0], [p + u, 1], [p - u, 1]])
    rp = Polygon(y2, facecolor="#aaffcc")

    ax.add_patch(lp)
    ax.add_patch(rp)

    ax.plot(
        [p - l - 0.8 * lu, p - 0.8 * u, p + r - 0.8 * ru],
        [0, 1, 0],
        linestyle="--",
        linewidth=0.7,
        c="#5555ff",
        label=K_PESSIMISTIC,
    )
    ax.plot(
        [p - l + 0.8 * lu, p + 0.8 * u, p + r + 0.8 * ru],
        [0, 1, 0],
        linestyle="--",
        linewidth=0.7,
        c="#ff5555",
        label=K_OPTIMISTIC,
    )
    ax.plot(
        [p - l, p, p + r],
        [0, 1, 0],
        linestyle=":",
        linewidth=2,
        c="k",
        label=K_EXPECTED,
    )
