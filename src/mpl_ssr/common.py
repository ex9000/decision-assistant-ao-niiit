import matplotlib

c_white = matplotlib.colors.colorConverter.to_rgba("white", alpha=0)
c_black = matplotlib.colors.colorConverter.to_rgba("black", alpha=1)

cmap_transparent2black = matplotlib.colors.LinearSegmentedColormap.from_list(
    "rb_cmap", [c_white, c_black], 512
)
