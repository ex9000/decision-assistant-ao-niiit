import flet as ft

from src.app.military.data_model import AnswerOption
from src.app.military.gui.forms import AnswerOptionEdit
from src.lang import *

items = []
free = set()


def window(page: ft.Page):
    switch_lang(Lang.RU)

    page.title = "СППР Аггрегация"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.scroll = ft.ScrollMode.

    page.add(
        AnswerOptionEdit(
            AnswerOption(
                MILITARY.ANSWER_OPTION.K_DEFAULT_SHORT_NAME.capitalize(),
                MILITARY.ANSWER_OPTION.K_DEFAULT_DESCRIPTION.capitalize(),
                str(MILITARY.ANSWER_OPTION.K_DEFAULT_CRITERIA),
                False,
            )
        ),
    )
    page.update()


def main():
    ft.app(window)


if __name__ == "__main__":
    main()
