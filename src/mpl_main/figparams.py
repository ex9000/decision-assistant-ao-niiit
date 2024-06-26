import io
from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple

from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


@dataclass
class FigParams:
    figsize: Tuple[float, float] = (6.0, 4.0)
    dpi: int = 200

    def init_ax_fig(self) -> Tuple[Figure, Axes]:
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        return fig, ax


class LegendType(Enum):
    DISABLED = auto()
    INSIDE = auto()
    OUTSIDE = auto()


NORMAL_FIG_PARAMS = FigParams()
WIDE_FIG_PARAMS = FigParams((12.0, 4.0))
SQUARE_FIG_PARAMS = FigParams((5.0, 5.0), dpi=100)


def final_patch(
        ax: Axes,
        /,
        legend: LegendType = LegendType.DISABLED,
        axes=True,
        grid=True,
        ax_labels: Tuple[str, str] = (None, None),
        title: str = None,
):
    if not axes:
        ax.set_axis_off()

    if axes and ax_labels[0]:
        ax.set_xlabel(ax_labels[0])

    if axes and ax_labels[1]:
        ax.set_ylabel(ax_labels[1])

    match legend:
        case LegendType.INSIDE:
            ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.95))
        case LegendType.OUTSIDE:
            ax.legend(
                loc="center left", bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True
            )

    if title:
        ax.set_title(title)

    if grid:
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
