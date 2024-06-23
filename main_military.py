import flet as ft

from src.app.military.data_model import AnswerOption
from src.app.military.gui.forms import AnswerOptionEdit

items = []
free = set()


def window(page: ft.Page):
    column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

    page.title = "СППР Аггрегация"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.scroll = ft.ScrollMode.

    page.add(
        AnswerOptionEdit(
            AnswerOption("short", "Main info", "# Main\n- the best", False)
        ),
    )
    page.update()


def main():
    ft.app(window)


if __name__ == "__main__":
    main()
