import flet as ft

items = []
free = set()


def window(page: ft.Page):
    column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

    page.title = "Тактическое планирование"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.scroll = ft.ScrollMode.

    page.add(
        ft.Image("./images/item.png", fit=ft.ImageFit.FIT_HEIGHT, height=200),
    )
    page.update()


def main():
    ft.app(window)


if __name__ == "__main__":
    main()
