import matplotlib.pyplot as plt

from src.fuzzy import TriangleSymmetric
from src.lang import switch_lang, Lang
from src.mpl_ssr import plot_bledge, NORMAL_FIG_PARAMS, final_patch, fig2pil
from src.probability import Normal


def main():
    switch_lang(Lang.RU)

    a = Normal(7, 1 / 9)
    delta = Normal(1, 0.01)
    X = TriangleSymmetric(-2, 4)

    fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

    # plot_bledge(ax, a + delta * X)
    # final_patch(ax)

    # ax.clear()
    #
    plot_bledge(ax, a + delta * X)
    final_patch(ax, legend=False, axes=True, grid=False)

    im = fig2pil(fig)

    im.show()

    plt.close(fig)
    ax.clear()
    fig.clear()
    del fig, ax


if __name__ == "__main__":
    main()
