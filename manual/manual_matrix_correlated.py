from itertools import groupby, pairwise, accumulate

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.mpl_corr import plot_matrix, best_figsize
from src.mpl_main import final_patch, fig2pil
from src.mpl_main.figparams import FigParams

words = [
    "none",
    "antialiased",
    "nearest",
    "bilinear",
    "bicubic",
    "spline16",
    "spline36",
    "hanning",
    "hamming",
    "hermite",
    "kaiser",
    "quadric",
    "catrom",
    "gaussian",
    "bessel",
    "mitchell",
    "sinc",
    "lanczos",
    "blackman",
]


def gensymmat(size, amplitude):
    """Generate symmetric matrix of given size."""
    matr = np.random.rand(size, size)
    matr += matr.T
    matr -= matr.min()
    if np.isclose(matr.max(), 0, atol=1e-8):
        matr += 1
    else:
        matr /= matr.max()
    return (2 * matr - 1) * amplitude


def main():
    np.random.seed(43)

    groups = accumulate(
        [0]
        + [
            len(list(items))
            for k, items in groupby(sorted(np.random.geometric(0.2, len(words)) % 5))
        ]
    )

    base = gensymmat(len(words), 0.1)
    for i, j in pairwise(groups):
        base[i:j, i:j] = np.random.choice([1, -1]) * (0.75 + gensymmat(j - i, 0.25))
    np.fill_diagonal(base, 0)

    pr = np.random.permutation(len(words))
    base = base[pr, :][:, pr]
    df = pd.DataFrame(base, columns=words, index=words)

    fig, ax = FigParams(figsize=best_figsize(len(words))).init_ax_fig()

    plot_matrix(ax, df)
    final_patch(ax, grid=False)
    im = fig2pil(fig)

    im.show()

    plt.close(fig)
    ax.clear()
    fig.clear()
    del fig, ax


if __name__ == "__main__":
    main()
