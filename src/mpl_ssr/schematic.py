import matplotlib.pyplot as plt

from src.fuzzy import TriangleSymmetric


def plot_schematic(ssr: TriangleSymmetric, title: str = ""):
    left = ssr.to_random(-1)
    mid = ssr.to_random(0)
    right = ssr.to_random(1)

    l, r = left.mu

    ax, fig = plt.subplots()
    ax.axhline(y=1, linestyle="-")
    ax.set_title(title)
    ax.set_xlabel("Effectiveness")
    ax.grid()
    ax.relim()
