import flet as ft
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from src.algebra import make_covariance
from src.app.basic_solution_support.data_model import Item, PRECISION_VALUES, FUZZY_WIDTH
from src.app.basic_solution_support.gui import new_item_card
from src.fuzzy import TriangleSymmetric
from src.lang import K_INCOME, K_RISK, K_FRONTIER_SHARES
from src.mpl_corr import best_figsize, plot_matrix
from src.mpl_main.figparams import (
    FigParams,
    final_patch,
    fig2pil,
    NORMAL_FIG_PARAMS,
    LegendType,
)
from src.mpl_shares import plot_shares_frontier
from src.probability import Normal
from src.tsn_ssr import compose_system, efficient_portfolio_frontier_no_shorts

items = []
free = set()


def solve():
    rands = [
        (
                Normal(0, PRECISION_VALUES[it.precision] ** 2)
                + TriangleSymmetric(it.usefulness, FUZZY_WIDTH)
        ).to_random(0)
        for it in items
    ]

    expected = np.array([r.mu for r in rands]) + np.random.random(size=len(rands)) * 0.1
    dispersion = np.array([r.sigma2 for r in rands])
    corr = np.eye(len(items))

    covariance = make_covariance(dispersion, corr)
    system = compose_system(expected, covariance)

    result, _ = efficient_portfolio_frontier_no_shorts(system)

    fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

    names = [it.name for it in items]
    plot_shares_frontier(ax, expected, covariance, names, result)

    final_patch(
        ax,
        legend=LegendType.OUTSIDE,
        ax_labels=(K_INCOME.title(), K_RISK.title()),
        title=K_FRONTIER_SHARES.capitalize(),
    )

    im = fig2pil(fig)

    im.show()

    plt.close(fig)
    ax.clear()
    fig.clear()
    del fig, ax


def corrs():
    base = np.eye(len(items))
    words = [it.name for it in items]

    df = pd.DataFrame(base, columns=words, index=words)

    fig, ax = FigParams(figsize=best_figsize(len(words))).init_ax_fig()

    plot_matrix(ax, df)
    final_patch(ax, grid=False)
    im = fig2pil(fig)

    im.show()

    plt.close(fig)
    ax.clear()
    fig.clear()
    del fig, ax


def window(page: ft.Page):
    column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

    page.title = "СППР Аггрегация"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT

    def drop_func(card, item):
        page.remove(card)
        items.remove(item)
        free.add(item.name)
        page.update()

    def plus_click(e):
        name = f"Item #{1 + len(items)}"
        if free:
            name = free.pop()

        items.append(Item(name))

        page.add(new_item_card(items[-1], drop_func))
        page.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=plus_click
    )

    page.scroll = ft.ScrollMode.HIDDEN

    page.add(
        ft.TextButton("Получить решение", on_click=lambda _: solve()),
        ft.TextButton("Настроить корреляции", on_click=lambda _: corrs()),
    )
    page.update()


def main():
    ft.app(window)


if __name__ == "__main__":
    main()
