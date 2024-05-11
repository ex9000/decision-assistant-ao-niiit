import numpy as np
from matplotlib.axes import Axes
from scipy.stats import rv_continuous

from src.fuzzy import TriangleSymmetric, Measure
from src.probability import Normal
from .plotting import prepare_plot


def _inverse_normalized(xs, dist: rv_continuous):
    v = dist.pdf(xs)
    v /= v.max()
    return 1 - v


def _evaluate(xs, left: rv_continuous, right: rv_continuous):
    return left.cdf(xs) * right.sf(xs)


def plot_density(ax: Axes, ssr: TriangleSymmetric[Normal], precision=256):
    left, right, source, xmax, xmin, xs, ys = prepare_plot(ax, precision, ssr)

    pairs = [
        (
            ssr.to_random(1 - alpha, Measure.NECESSITY).to_scipy_stat(),
            ssr.to_random(alpha, Measure.POSSIBILITY).to_scipy_stat(),
        )
        for alpha in ys
    ]

    data = np.stack([_evaluate(xs, left, right) for left, right in pairs])

    ax.pcolormesh(*source, data, shading="gouraud", cmap="Greys")
    cs = ax.contour(*source, data, cmap="plasma")
    ax.clabel(cs, inline=1, fontsize=10)
