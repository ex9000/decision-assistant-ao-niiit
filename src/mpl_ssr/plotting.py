import numpy as np


def prepare_plot(ax, precision, ssr):
    left = ssr.to_random(-1)
    right = ssr.to_random(1)

    sigmas = 3

    xmin, xmax = (
        left.mu - sigmas * left.sigma2 ** 0.5,
        right.mu + sigmas * right.sigma2 ** 0.5,
    )

    xs = np.linspace(xmin, xmax, precision)
    ys = np.linspace(0, 1, precision)

    source = np.meshgrid(xs, ys)

    # hack to expand y-limit
    ax.plot((xmin, xmax), (-0.01, 1.01), alpha=0)

    return left, right, source, xmax, xmin, xs, ys
