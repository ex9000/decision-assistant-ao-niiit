import numpy as np
from matplotlib import pyplot as plt

from src.algebra import make_covariance
from src.lang import *
from src.mpl_main import NORMAL_FIG_PARAMS, final_patch, LegendType, fig2pil
from src.mpl_shares import plot_shares_frontier
from src.tsn_ssr import compose_system, efficient_portfolio_frontier_no_shorts

size = 10
np.random.seed(49)

expected = np.random.randint(1, 15, size=size) + np.random.random(size) * 0.1
dispersion = np.random.randint(1, 15, size=size) + np.random.random(size) * 0.1

assert len(set(zip(dispersion, expected))) == size

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors ** 2).sum(axis=0))
corr = vectors.T @ vectors

covariance = make_covariance(dispersion, corr)

system = compose_system(expected, covariance)

result, _ = efficient_portfolio_frontier_no_shorts(system)
print(result)

switch_lang(Lang.RU)

fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
plot_shares_frontier(ax, expected, covariance, names, result)

final_patch(
    ax,
    legend=LegendType.OUTSIDE,
    ax_labels=(K_INCOME.title(), K_RISK.title()),
    title=K_FRONTIER_SHARES.capitalize(),
)

im = fig2pil(fig)

im.show()

plt.close(fig)
ax.clear()
fig.clear()
del fig, ax
