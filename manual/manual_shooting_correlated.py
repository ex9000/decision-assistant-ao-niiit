import matplotlib.pyplot as plt

from src.mpl_corr import plot_shooting_target
from src.mpl_main import SQUARE_FIG_PARAMS, final_patch, fig2pil


def main():
    corr = -0.8

    fig, ax = SQUARE_FIG_PARAMS.init_ax_fig()

    plot_shooting_target(ax, corr)

    final_patch(ax, legend=False, axes=False)

    im = fig2pil(fig)

    im.show()

    plt.close(fig)
    ax.clear()
    fig.clear()
    del fig, ax


if __name__ == "__main__":
    main()
