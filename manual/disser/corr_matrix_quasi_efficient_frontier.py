import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from src.algebra import (
    make_covariance,
)
from src.lang import *
from src.mpl_corr import plot_matrix
from src.mpl_main import (
    SQUARE_FIG_PARAMS,
)
from src.tsn_ssr import (
    compose_system,
    efficient_portfolio_frontier_no_shorts,
)

# (5, 15, 44) (5, 15, 43 back)
size, rng, seed = 5, 15, 42
np.random.seed(seed)

expected = np.random.randint(1, rng, size=size) + np.random.random(size) * 0.1
dispersion = np.random.randint(1, rng, size=size) + np.random.random(size) * 0.1

assert len(set(zip(dispersion, expected))) == size

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors**2).sum(axis=0))

perm = [x - 1 for x in [3, 2, 5, 1, 4]]
# perm = [x - 1 for x in [2, 1, 5, 3, 4]]
expected = expected[perm]
dispersion = dispersion[perm]
vectors = vectors[..., perm]

expected = expected.round(0)
dispersion = dispersion.round(0)

# corr = np.eye(size)
corr = vectors.T @ vectors
corr = corr.round(1)

covariance = make_covariance(dispersion, corr)

system = compose_system(expected, covariance)

result, _ = efficient_portfolio_frontier_no_shorts(system)
print(result)

switch_lang(Lang.RU)

fig, ax = SQUARE_FIG_PARAMS.init_ax_fig()


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

df = pd.DataFrame(corr, columns=names[:size], index=names[:size])
plot_matrix(ax, df, "{:+.0%}")

print(f"{expected=}")
print(f"{dispersion=}")


fig.tight_layout()

plt.show()
plt.close(fig)
