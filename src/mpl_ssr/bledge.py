import numpy as np
from matplotlib.axes import Axes
from scipy.stats import rv_continuous

from src.fuzzy import TriangleSymmetric, Measure
from src.mpl_ssr.plotting import prepare_plot
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
    left, right, source, xmax, xmin, xs, ys = prepare_plot(ax, precision, ssr)

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

    ax.pcolormesh(*source, data, shading="gouraud", cmap="Greys")
