import numpy as np
from matplotlib.axes import Axes
from scipy.stats import rv_continuous

from src.fuzzy import TriangleSymmetric, Measure
from src.probability import Normal


def _inverse_normalized(xs, dist: rv_continuous):
    v = dist.pdf(xs)
    v /= v.max()
    return 1 - v


def _evaluate(xs, y, left: rv_continuous, right: rv_continuous):
    a = _inverse_normalized(xs, left)
    b = _inverse_normalized(xs, right)

    # eliminate an illusion of bright vertical line
    smooth = 1 - (a ** 0.5 * b ** 0.5) ** 2
    ground_truth = 1 - np.minimum(a, b)

    k = y ** 16

    return (1 - k) * smooth + k * ground_truth


def plot_bledge(ax: Axes, ssr: TriangleSymmetric[Normal], precision=256):
    left = ssr.to_random(-1)
    right = ssr.to_random(1)

    xmin, xmax = left.mu - 2 * left.sigma2 ** 0.5, right.mu + 2 * right.sigma2 ** 0.5

    ys = np.linspace(0, 1, precision)
    xs = np.linspace(xmin, xmax, precision)

    pairs = {
        alpha: (
            ssr.to_random(alpha, Measure.NECESSITY).to_scipy_stat(),
            ssr.to_random(1 - alpha, Measure.POSSIBILITY).to_scipy_stat(),
        )
        for alpha in ys
    }

    data = np.stack(
        [_evaluate(xs, y, left, right) for y, (left, right) in pairs.items()]
    )

    source = np.meshgrid(xs, ys)

    ax.pcolormesh(*source, data, shading="gouraud", cmap="gray_r")

    # hack to expand y-limit
    ax.plot((xmin, xmax), (-0.01, 1.01), alpha=0)