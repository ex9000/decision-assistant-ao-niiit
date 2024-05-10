import numpy as np
from matplotlib.axes import Axes
from scipy.stats import rv_continuous

from src.fuzzy import TriangleSymmetric, Measure
from src.probability import Normal


def _inverse_normalized(xs, dist: rv_continuous):
    v = dist.pdf(xs)
    v /= v.max()
    return 1 - v


def _evaluate(xs, left: rv_continuous, right: rv_continuous):
    return left.cdf(xs) * right.sf(xs)


def plot_density(ax: Axes, ssr: TriangleSymmetric[Normal], precision=256):
    left = ssr.to_random(-1)
    right = ssr.to_random(1)

    xmin, xmax = left.mu - 2 * left.sigma2 ** 0.5, right.mu + 2 * right.sigma2 ** 0.5

    xs = np.linspace(xmin, xmax, precision)
    ys = np.linspace(0, 1, precision)

    pairs = [
        (
            ssr.to_random(alpha, Measure.NECESSITY).to_scipy_stat(),
            ssr.to_random(1 - alpha, Measure.POSSIBILITY).to_scipy_stat(),
        )
        for alpha in ys
    ]

    data = np.stack([_evaluate(xs, left, right) for left, right in pairs])

    source = np.meshgrid(xs, ys)

    ax.pcolormesh(*source, data, shading="gouraud", cmap="gray_r")
    cs = ax.contour(*source, data, cmap="plasma")
    ax.clabel(cs, inline=1, fontsize=10)

    # hack to expand y-limit
    ax.plot((xmin, xmax), (-0.01, 1.01), alpha=0)
