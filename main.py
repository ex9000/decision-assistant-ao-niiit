import flet as ft

from src.square_root import solve


def window(page: ft.Page):
    counter = 0

    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    txt_number = ft.TextField(value="0")

    def minus_click(e):
        nonlocal counter
        counter -= 1

        _, root = solve(1, 0, -counter)
        txt_number.value = str(root)
        page.update()

    def plus_click(e):
        nonlocal counter
        counter += 1

        _, root = solve(1, 0, -counter)
        txt_number.value = str(root)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


def main():
    ft.app(window)


if __name__ == "__main__":
    main()
