import matplotlib.pyplot as plt

from src.fuzzy import TriangleSymmetric
from src.lang import *
from src.mpl_main import NORMAL_FIG_PARAMS, final_patch, fig2pil
from src.mpl_main.figparams import LegendType
from src.mpl_ssr import plot_schematic
from src.probability import Normal


def main():
    switch_lang(Lang.RU)

    a = Normal(7, 1)
    delta = Normal(10, 16)
    X = TriangleSymmetric(1, 4)

    fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

    plot_schematic(ax, a + delta * X)
    final_patch(
        ax,
        legend=LegendType.INSIDE,
        ax_labels=(K_EFFECTIVENESS.title(), K_POSSIBILITY.title()),
    )

    im = fig2pil(fig)

    im.show()

    plt.close(fig)
    ax.clear()
    fig.clear()
    del fig, ax


if __name__ == "__main__":
    main()
