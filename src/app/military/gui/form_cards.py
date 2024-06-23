import flet as ft

from src.app.military.data_model import AnswerOption


class AnswerOptionCard(ft.Card):
    def __init__(self, answer_option: AnswerOption):
        super().__init__()

        self.answer_option = answer_option

        self.content = ft.Container(
            padding=10,
            content=ft.Row(
                [
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_UP),
                                    ft.IconButton(
                                        icon=ft.icons.KEYBOARD_DOUBLE_ARROW_UP
                                    ),
                                ]
                            ),
                            ft.Text(
                                self.answer_option.short,
                                style=ft.TextThemeStyle.TITLE_LARGE,
                            ),
                            ft.Text(
                                self.answer_option.info,
                                style=ft.TextThemeStyle.TITLE_SMALL,
                            ),
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_DOWN),
                                    ft.IconButton(
                                        icon=ft.icons.KEYBOARD_DOUBLE_ARROW_DOWN
                                    ),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Markdown(self.answer_option.criteria),
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.IconButton(icon=ft.icons.EDIT),
                            ft.IconButton(icon=ft.icons.DELETE),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ]
            ),
        )
