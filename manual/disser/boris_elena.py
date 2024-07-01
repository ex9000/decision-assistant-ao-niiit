from matplotlib import pyplot as plt

from src.fuzzy import TriangleSymmetric
from src.mpl_main import WIDE_FIG_PARAMS
from src.mpl_ssr import plot_density
from src.probability import Normal

boris = Normal(3, 0.4) + Normal(4, 5) * TriangleSymmetric(0.1, 1)
elena = Normal(11, 1.2) + Normal(12, 13) * TriangleSymmetric(0.6, 1)


fig, ax = WIDE_FIG_PARAMS.init_ax_fig()

plot_density(ax, boris)
plot_density(ax, elena)


fig.tight_layout()


plt.show()
