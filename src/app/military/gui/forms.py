import flet as ft

from src.app.military.data_model import AnswerOption
from src.lang import *
from .version_control import VersionControl


class AnswerOptionEdit(ft.Column):
    def __init__(self, answer_option: AnswerOption):
        super().__init__()

        self.answer_option = answer_option

        self.back_bt = ft.IconButton(icon=ft.icons.ARROW_BACK)
        self.short_edit = ft.TextField(
            label=K_SHORT_NAME.capitalize(),
            hint_text=K_OPTION_SHORT_NAME_HINT.capitalize(),
            on_change=self.short_change,
            expand=True,
        )
        self.info_edit = ft.TextField(
            multiline=True,
            label=K_DESCRIPTION.capitalize(),
            hint_text=K_OPTION_DESCRIPTION_HINT.capitalize(),
            on_change=self.info_change,
        )
        self.criteria_edit = ft.TextField(
            multiline=True,
            label=K_CRITERIA.capitalize(),
            hint_text=K_OPTION_CRITERIA_HINT.capitalize(),
            max_lines=10,
            on_change=self.criteria_change,
        )
        self.save_bt = ft.FilledTonalButton(
            K_SAVE.capitalize(),
            disabled=True,
            on_click=self.save_click,
        )

        self.version_control = VersionControl(answer_option, callback=self.update)

        self.controls = [
            self.back_bt,
            ft.Row(
                controls=[
                    self.short_edit,
                    ft.Container(padding=ft.padding.symmetric(horizontal=50)),
                    self.version_control,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            self.info_edit,
            self.criteria_edit,
            self.save_bt,
        ]

    def short_change(self, *_):
        self.answer_option.short = self.short_edit.value
        self.save_bt.disabled = False
        self.save_bt.update()

    def info_change(self, *_):
        self.answer_option.info = self.info_edit.value
        self.save_bt.disabled = False
        self.save_bt.update()

    def criteria_change(self, *_):
        self.answer_option.criteria = self.criteria_edit.value
        self.save_bt.disabled = False
        self.save_bt.update()

    def save_click(self, *_):
        self.answer_option.commit()
        self.save_bt.disabled = True
        self.update()

    def before_update(self):
        self.short_edit.value = self.answer_option.short
        self.info_edit.value = self.answer_option.info
        self.criteria_edit.value = self.answer_option.criteria
