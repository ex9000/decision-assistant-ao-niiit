import flet as ft

from src.app.data_model import Item
from src.app.gui import new_item_card

items = []
free = set()


def window(page: ft.Page):
    column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

    page.title = "СППР Аггрегация"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT

    def drop_func(card, item):
        column.controls.remove(card)
        items.remove(item)
        free.add(item.name)
        page.update()

    def plus_click(e):
        name = f"Item #{1 + len(items)}"
        if free:
            name = free.pop()

        items.append(Item(name, 0, 0))

        column.controls.append(new_item_card(items[-1], drop_func))
        page.update()

    page.add(
        ft.Column(
            [
                column,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


def main():
    ft.app(window)


if __name__ == "__main__":
    main()
