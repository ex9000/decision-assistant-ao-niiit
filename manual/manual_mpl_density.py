import matplotlib.pyplot as plt

from src.fuzzy import TriangleSymmetric
from src.lang import switch_lang, Lang
from src.mpl_ssr import plot_density, NORMAL_FIG_PARAMS, final_patch, fig2pil
from src.probability import Normal


def main():
    switch_lang(Lang.RU)

    a = Normal(7, 1)
    delta = Normal(10, 16)
    X = TriangleSymmetric(1, 4)

    fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

    plot_density(ax, a + delta * X)
    final_patch(ax, legend=False, axes=True)

    im = fig2pil(fig)

    im.show()

    plt.close(fig)
    ax.clear()
    fig.clear()
    del fig, ax


if __name__ == "__main__":
    main()
