import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from src.mpl_corr import plot_matrix, best_figsize
from src.mpl_main.figparams import FigParams

size, seed = 10, 42
np.random.seed(seed)

vectors = np.random.random((size, size)) - 0.5
vectors /= np.sqrt((vectors**2).sum(axis=0))

corr = vectors.T @ vectors
corr = corr.round(2)

fig, ax = FigParams(best_figsize(size), 300).init_ax_fig()


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
plot_matrix(ax, df, "{:+.0%}", "xx-small")

fig.tight_layout()

plt.show()
plt.close(fig)
