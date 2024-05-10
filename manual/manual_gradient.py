import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.patches import Polygon

fig, ax = plt.subplots(1)

verts = np.random.rand(3, 2)
xmin, xmax = verts[:, 0].min(), verts[:, 0].max()
ymin, ymax = verts[:, 1].min(), verts[:, 1].max()

cmap = colors.LinearSegmentedColormap.from_list("white_to_red", ["white", "red"])
grad = np.atleast_2d(np.linspace(0, 1, 256)).T
img = ax.imshow(
    np.flip(grad),
    extent=[xmin, xmax, ymin, ymax],
    interpolation="nearest",
    aspect="auto",
    cmap=cmap,
)
polygon = Polygon(verts, closed=True, facecolor="none", edgecolor="none")
ax.add_patch(polygon)
# img.set_clip_path(polygon)

ax.autoscale_view()
plt.show()
