from functools import partial

import flet as ft
from flet_multi_page import subPage

from src.app.data_model import Item


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


def start_edit_item_dialog(item: Item):
    p = subPage(target=partial(setup_edit_item_dialog, item))
    p.start()
