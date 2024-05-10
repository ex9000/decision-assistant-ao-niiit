from math import pi, sqrt

import numpy as np
from matplotlib.axes import Axes
from scipy.stats import rv_continuous

from src.fuzzy import TriangleSymmetric, Measure
from src.probability import Normal


@np.vectorize(excluded=("pairs",))
def _evaluate(x, y, pairs: dict[float, tuple[rv_continuous, rv_continuous]]):
    left, right = pairs[y]
    left: rv_continuous
    right: rv_continuous

    a = 1 - left.pdf(x) * sqrt(2 * pi * left.var())
    b = 1 - right.pdf(x) * sqrt(2 * pi * right.var())

    p = 1 - (a ** 0.5 * b ** 0.5) ** 2
    q = 1 - min(a, b)

    return np.interp(y ** 16, (0, 1), (p, q))


def plot_bledge(ax: Axes, ssr: TriangleSymmetric[Normal], precision=64):
    left = ssr.to_random(-1)
    right = ssr.to_random(1)

    xmin, xmax = left.mu - 3 * left.sigma2 ** 0.5, right.mu + 3 * right.sigma2 ** 0.5

    ys = np.linspace(0, 1, precision)
    pairs = {
        alpha: (
            ssr.to_random(alpha, Measure.NECESSITY).to_scipy_stat(),
            ssr.to_random(1 - alpha, Measure.POSSIBILITY).to_scipy_stat(),
        )
        for alpha in ys
    }

    source = np.meshgrid(np.linspace(xmin, xmax, precision), ys)  # , indexing="ij")
    data = _evaluate(
        *source,
        pairs=pairs,
    )

    ax.pcolormesh(*source, data, shading="gouraud", cmap="gray_r")
