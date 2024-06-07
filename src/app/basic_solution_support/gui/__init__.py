import base64
from functools import partial

import flet as ft
from PIL.Image import Image
from flet_multi_page import subPage
from matplotlib import pyplot as plt

from src.app.basic_solution_support.data_model import Item, PRECISION_VALUES, FUZZY_WIDTH
from src.fuzzy import TriangleSymmetric
from src.lang import *
from src.mpl_main import NORMAL_FIG_PARAMS, final_patch, fig2pil
from src.mpl_ssr import plot_density
from src.probability import Normal


def new_item_card(item: Item, drop_func):
    card = ft.Row(
        [
            ft.TextField(item.name),
            ft.IconButton(
                ft.icons.EDIT, on_click=lambda _: start_edit_item_dialog(item)
            ),
            ft.IconButton(ft.icons.DELETE, on_click=lambda _: drop_func(card, item)),
        ]
    )
    return card


def setup_edit_item_dialog(item: Item, page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = item.name
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.HIDDEN

    # page.on_window_event = lambda e: print(e.data)

    def update():
        switch_lang(Lang.RU)

        a = Normal(0, PRECISION_VALUES[item.precision] ** 2)
        X = TriangleSymmetric(item.usefulness, FUZZY_WIDTH)

        fig, ax = NORMAL_FIG_PARAMS.init_ax_fig()

        plot_density(ax, a + X)
        final_patch(ax, ax_labels=(K_EFFECTIVENESS.title(), K_POSSIBILITY.title()))

        for i, c in zip(range(4), ["red", "orange", "yellow", "green"]):
            ax.plot(
                [i - FUZZY_WIDTH / 2, i, i + FUZZY_WIDTH / 2],
                [0, 1, 0],
                c=c,
                linewidth=0.5,
                linestyle="--",
            )

        im: Image = fig2pil(fig)

        im.save("./images/item.png")

        plt.close(fig)
        ax.clear()
        fig.clear()
        del fig, ax

    update()
    image = ft.Image(
        src_base64=base64.b64encode(open("./images/item.png", "br").read()).decode(
            "utf-8"
        ),
        fit=ft.ImageFit.CONTAIN,
    )

    def handel_usefulness(e):
        nonlocal image
        item.usefulness = int(e.data[2:-2])  # wtf list as string
        update()
        image.src_base64 = base64.b64encode(
            open("./images/item.png", "br").read()
        ).decode("utf-8")
        page.update()

    def handel_precision(e):
        nonlocal image
        item.precision = int(e.data[2:-2])  # wtf list as string
        update()
        image.src_base64 = base64.b64encode(
            open("./images/item.png", "br").read()
        ).decode("utf-8")
        page.update()

    page.add(
        ft.Text("Полезность"),
        ft.SegmentedButton(
            selected_icon=ft.Icon(ft.icons.DONE),
            selected={str(item.usefulness)},
            on_change=handel_usefulness,
            segments=[
                ft.Segment(
                    value="0",
                    label=ft.Text("Плохая"),
                    icon=ft.Icon(ft.icons.SQUARE_OUTLINED),
                ),
                ft.Segment(
                    value="1",
                    label=ft.Text("Нормальная"),
                    icon=ft.Icon(ft.icons.SQUARE_OUTLINED),
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("Хоршая"),
                    icon=ft.Icon(ft.icons.SQUARE_OUTLINED),
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("Отличная"),
                    icon=ft.Icon(ft.icons.SQUARE_OUTLINED),
                ),
            ],
        ),
        ft.Text("Точность"),
        ft.SegmentedButton(
            selected_icon=ft.Icon(ft.icons.DONE),
            selected={str(item.precision)},
            on_change=handel_precision,
            segments=[
                ft.Segment(
                    value="0",
                    label=ft.Text("Низкая"),
                    icon=ft.Icon(ft.icons.SQUARE_OUTLINED),
                ),
                ft.Segment(
                    value="1",
                    label=ft.Text("Сомнительная"),
                    icon=ft.Icon(ft.icons.SQUARE_OUTLINED),
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("Высокая"),
                    icon=ft.Icon(ft.icons.SQUARE_OUTLINED),
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("Превосходная"),
                    icon=ft.Icon(ft.icons.SQUARE_OUTLINED),
                ),
            ],
        ),
        image,
    )


def start_edit_item_dialog(item: Item):
    p = subPage(target=partial(setup_edit_item_dialog, item))
    p.start()
