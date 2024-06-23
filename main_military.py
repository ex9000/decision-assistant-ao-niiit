import flet as ft

from src.app.military.data_model import AnswerOption, FormItem, FormGroup
from src.app.military.gui.forms import FormItemEdit
from src.lang import *

items = []
free = set()


def window(page: ft.Page):
    switch_lang(Lang.RU)

    page.title = "СППР Аггрегация"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.scroll = ft.ScrollMode.HIDDEN

    fgroup1 = FormGroup("I. Short", "Info")
    fgroup2 = FormGroup("II. Short", "Info")
    fgroup3 = FormGroup("III. Short", "Info")

    fitem = FormItem(
        "text",
        "description",
        fgroup1,
        [
            AnswerOption(
                "I. " + MILITARY.ANSWER_OPTION.K_DEFAULT_SHORT_NAME.capitalize(),
                MILITARY.ANSWER_OPTION.K_DEFAULT_DESCRIPTION.capitalize(),
                str(MILITARY.ANSWER_OPTION.K_DEFAULT_CRITERIA),
                False,
            ),
            AnswerOption(
                "II. " + MILITARY.ANSWER_OPTION.K_DEFAULT_SHORT_NAME.capitalize(),
                MILITARY.ANSWER_OPTION.K_DEFAULT_DESCRIPTION.capitalize(),
                str(MILITARY.ANSWER_OPTION.K_DEFAULT_CRITERIA),
                False,
            ),
            AnswerOption(
                "III. " + MILITARY.ANSWER_OPTION.K_DEFAULT_SHORT_NAME.capitalize(),
                MILITARY.ANSWER_OPTION.K_DEFAULT_DESCRIPTION.capitalize(),
                str(MILITARY.ANSWER_OPTION.K_DEFAULT_CRITERIA),
                False,
            ),
        ],
        False,
    )

    page.add(
        FormItemEdit(fitem, [fgroup1, fgroup2, fgroup3]),
    )
    page.update()


def main():
    ft.app(window)


if __name__ == "__main__":
    main()
