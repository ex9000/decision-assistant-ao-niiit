from matplotlib import pyplot as plt

from src.fit_ssr import fit_crisp_cslsr
from src.mpl_main import NORMAL_FIG_PARAMS
from src.mpl_ssr import plot_bledge
from src.probability import Normal

central = Normal(13, 0.5)
dleft = Normal(14, 3)
dright = Normal(10, 9)
full_fit = fit_crisp_cslsr(central, dleft, dright)


left = central - dleft
right = central + dright

mini = left.mu - 3 * left.sigma2**0.5
maxi = right.mu + 3 * right.sigma2**0.5

fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

plot_bledge(ax, full_fit)

plt.scatter(
    [left.mu, central.mu, right.mu],
    [0, 1, 0],
    c="r",
    zorder=100,
)

plt.text(left.mu, -0.045, r"$\psi(\omega)-\xi(\omega)$", va="top", ha="center")
plt.annotate(
    text="",
    c="k",
    xy=(left.mu - 3 * left.sigma2**0.5, -0.03),
    xytext=(left.mu + 3 * left.sigma2**0.5, -0.03),
    arrowprops=dict(arrowstyle="<->"),
)

plt.text(right.mu, -0.045, r"$\psi(\omega)+\zeta(\omega)$", va="top", ha="center")
plt.annotate(
    text="",
    c="k",
    xy=(right.mu - 3 * right.sigma2**0.5, -0.03),
    xytext=(right.mu + 3 * right.sigma2**0.5, -0.03),
    arrowprops=dict(arrowstyle="<->"),
)

plt.text(central.mu, 1 + 0.04, r"$\psi(\omega)$", va="bottom", ha="center")
plt.annotate(
    text="",
    c="k",
    xy=(central.mu - 3 * central.sigma2**0.5, 1 + 0.025),
    xytext=(central.mu + 3 * central.sigma2**0.5, 1 + 0.025),
    arrowprops=dict(arrowstyle="<->"),
)

for sp in ax.spines.values():
    sp.set_visible(False)

ax.spines["left"].set_visible(True)
ax.axes.get_xaxis().set_visible(False)

ax.set_xlim(left=mini, right=maxi)


plt.show()
