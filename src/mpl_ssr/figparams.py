import io
from dataclasses import dataclass
from typing import Tuple

from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.lang import *


@dataclass
class FigParams:
    figsize: Tuple[float, float] = (6.0, 4.0)
    dpi: int = 200

    def init_ax_fig(self) -> Tuple[Figure, Axes]:
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        return fig, ax


NORMAL_FIG_PARAMS = FigParams()
WIDE_FIG_PARAMS = FigParams((12.0, 4.0))


def final_patch(ax: Axes, /, legend=False, axes=False):
    ax.axhline(y=1, linestyle="-", c="black", linewidth=2.0)

    if axes:
        ax.set_xlabel(K_EFFECTIVENESS.title())
        ax.set_ylabel(K_EFFECTIVENESS.title())

    if legend:
        ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.95))

    ax.grid()
    ax.relim()


def fig2pil(fig: Figure, /, tight=True) -> Image:
    if tight:
        fig.tight_layout()
    fig.canvas.draw()

    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)

    im = Image.open(buf)
    return im
