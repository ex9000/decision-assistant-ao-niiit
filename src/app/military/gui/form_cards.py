import flet as ft

from src.app.military.data_model import AnswerOption, FormItem


class AnswerOptionCard(ft.Card):
    def __init__(self, answer_option: AnswerOption, form_item: FormItem):
        super().__init__()

        self.answer_option = answer_option
        self.form_item = form_item
        self.key = self.answer_option.uid.hex

        self.title_row = ft.Row(
            controls=[
                ft.Text(
                    self.answer_option.short,
                    style=ft.TextThemeStyle.TITLE_LARGE,
                )
            ]
        )

        self.up_bt = ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_UP)
        self.top_bt = ft.IconButton(icon=ft.icons.KEYBOARD_DOUBLE_ARROW_UP)
        self.down_bt = ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_DOWN)
        self.bottom_bt = ft.IconButton(icon=ft.icons.KEYBOARD_DOUBLE_ARROW_DOWN)

        self.content = ft.Container(
            padding=10,
            content=ft.Row(
                [
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    self.up_bt,
                                    self.top_bt,
                                ]
                            ),
                            self.title_row,
                            ft.Text(
                                self.answer_option.info,
                                style=ft.TextThemeStyle.TITLE_SMALL,
                            ),
                            ft.Row(
                                controls=[
                                    self.down_bt,
                                    self.bottom_bt,
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
