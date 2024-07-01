import numpy as np
import pandas as pd
from matplotlib import cm as mpl_cm
from matplotlib.axes import Axes
from numpy.polynomial.polynomial import polyval

from src.algebra import quadratic_form


def plot_shares_frontier(ax: Axes, expected, covariance, names: list[str], result):
    size = len(expected)
    V = expected
    M = covariance
    data = pd.DataFrame(result).to_dict(orient="list")

    lx, hx = min(V), max(V)
    xx = hx - lx
    lx -= 0.15 * xx
    hx += 0.15 * xx

    ly, hy = 0, np.diag(M).max()
    yy = hy - ly
    hy += 0.10 * yy

    xs = np.linspace(lx, hx, 1000)

    # fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()
    # ax.set_title("Frontier with shares")
    # ax.grid(True)

    indices = range(size)
    # names = list(map(str, range(size)))

    dcolors = np.array(mpl_cm.tab10.colors)
    dcolors = dcolors ** np.full(dcolors.shape, 0.2)
    dcolors = dict(zip(indices, dcolors))

    ax.scatter(V, np.diag(M), c="black", zorder=100)
    for txt, x, y in zip(names, V, np.diag(M)):
        ax.annotate(txt.title(), (x, y), zorder=100)

    labeled = {i: False for i in indices}
    for idx, poly, (mn, mx), (x, y) in zip(
        data["index"], data["poly"], data["segment"], data["point"]
    ):

        ws = polyval(xs, poly)
        ys = quadratic_form(M, ws)

        if mn <= x <= mx:
            ax.axvline(x=x, c="black", linestyle="--")

        has_label = [i for i in idx if not labeled[i]]
        for i in idx:
            labeled[i] = True

        dotted = (mn <= xs) & (xs <= mx) & (xs <= x)
        solid = (mn <= xs) & (xs <= mx) & (xs >= x)

        if np.any(dotted):
            ax.plot(xs[dotted], ys[dotted], color="black", linestyle=":")

        if np.any(solid):
            ax.plot(xs[solid], ys[solid], color="black")

        ax.axvline(x=mn, lw=0.7, c="red", linestyle="--")
        ax.axvline(x=mx, lw=0.7, c="red", linestyle="--")

        vals = polyval(np.array([mn, mx]), poly).T
        vals = np.concatenate([np.zeros((2, 1)), vals], axis=1)
        vals = vals.cumsum(axis=1) * hy * 0.90

        outline = False
        for i in idx:
            args = ([mn, mx], vals[..., i], vals[..., i + 1])
            if i != idx[-1]:
                ax.plot(args[0], args[2], c="black", linestyle="--", lw=0.7, zorder=5)
            outline = True
            if i in has_label:
                ax.fill_between(
                    *args,
                    color=dcolors[i % len(dcolors)],
                    label=names[i] if i < len(names) else f"{i=}",
                )
            else:
                ax.fill_between(*args, color=dcolors[i % len(dcolors)])

    # ax.legend()
    # ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
    # fig.tight_layout()

    # plt.show()
