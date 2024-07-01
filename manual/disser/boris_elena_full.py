import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import polyval

from src.algebra import make_covariance
from src.fuzzy import TriangleSymmetric
from src.lang import K_EXPECTED_VALUE, K_DISPERSION, switch_lang, Lang
from src.mpl_corr import best_figsize, plot_matrix
from src.mpl_main.figparams import FigParams, NORMAL_FIG_PARAMS, final_patch, LegendType
from src.mpl_shares import plot_shares_frontier
from src.probability import Normal
from src.tsn_ssr import (
    tsn_dispersion,
    tsn_expected_polynomials,
    compose_system,
    efficient_portfolio_frontier_no_shorts,
)

size, seed = 10, 42

assets = [
    Normal(i, 0.1 * (i + 1)) + Normal(i + 1, i + 2) * TriangleSymmetric(0.1 * i, 1)
    for i in range(1, 2 * size, 2)
]

expected = polyval(0.5, tsn_expected_polynomials(assets))
dispersion = tsn_dispersion(assets).round(2)


np.random.seed(seed)

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors**2).sum(axis=0))

corr = vectors.T @ vectors
corr = corr.round(2)

covariance = make_covariance(dispersion, corr)
system = compose_system(expected, covariance)

fig, ax = FigParams(best_figsize(size), 300).init_ax_fig()


print(f"{expected=}")
print(f"{dispersion=}")

names = [
    "Анна",
    "Борис",
    "Василий",
    "Григорий",
    "Дмитрий",
    "Елена",
    "Женя",
    "Зинаида",
    "Иван",
    "Константин",
    "Леонид",
    "Михаил",
    "Николай",
    "Ольга",
    "Павел",
    "Роман",
    "Семён",
    "Татьяна",
    "Ульяна",
    "Фёдор",
    "Харитон",
    "Шура",
    "Юрий",
    "Яков",
]

tail = ["Мат. Ожидание", "Нормализация"]
df = pd.DataFrame(system, columns=names[:size] + tail, index=names[:size] + tail)
plot_matrix(
    ax,
    df,
    values_format="{:.0f}",
    fontsize="x-small",
    clustering=False,
    scale=np.abs(system).max(),
)

fig.tight_layout()

plt.show()
plt.close(fig)


switch_lang(Lang.RU)
result, _ = efficient_portfolio_frontier_no_shorts(system)
fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()
plot_shares_frontier(ax, expected, covariance, names, result)
final_patch(
    ax,
    legend=LegendType.OUTSIDE,
    ax_labels=(K_EXPECTED_VALUE.title(), K_DISPERSION.title()),
)

fig.tight_layout()

plt.show()
plt.close(fig)
