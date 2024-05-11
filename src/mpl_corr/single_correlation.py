import numpy as np
from matplotlib.axes import Axes
from scipy.stats import gaussian_kde


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
    ax.clabel(cs, inline=1, fontsize=14)
