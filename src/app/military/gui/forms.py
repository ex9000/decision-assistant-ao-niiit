import flet as ft

from src.app.military.data_model import AnswerOption, FormItem
from src.lang import *
from .form_cards import AnswerOptionCard
from .version_control import VersionControl


class AnswerOptionEdit(ft.Column):
    def __init__(self, answer_option: AnswerOption):
        super().__init__()

        self.answer_option = answer_option

        self.back_bt = ft.IconButton(icon=ft.icons.ARROW_BACK)
        self.save_bt = ft.FilledTonalButton(
            K_SAVE.capitalize(),
            disabled=True,
            on_click=self.save_click,
        )

        self.short_edit = ft.TextField(
            label=K_SHORT_NAME.capitalize(),
            hint_text=K_OPTION_SHORT_NAME_HINT.capitalize(),
            on_change=self.short_change,
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
            min_lines=3,
            max_lines=10,
            on_change=self.criteria_change,
        )

        self.version_control = VersionControl(answer_option, callback=self.update)

        self.controls = [
            ft.Row(
                controls=[self.back_bt, self.version_control],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            self.short_edit,
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


class FormItemEdit(ft.Column):
    def __init__(self, form_item: FormItem):
        super().__init__()
        self.form_item = form_item
        self.group = form_item.group

        self.expand = True

        self.back_bt = ft.IconButton(icon=ft.icons.ARROW_BACK)
        self.save_bt = ft.FilledTonalButton(
            K_SAVE.capitalize(),
            disabled=True,
            on_click=self.save_click,
        )
        self.version_control = VersionControl(form_item, callback=self.update)

        self.text_edit = ft.TextField()

        self.description_edit = ft.TextField(
            multiline=True,
            min_lines=3,
            max_lines=10,
        )

        self.reverse_bt = ft.FilledTonalButton(icon=ft.icons.SWAP_VERT, text="Reverse")
        self.best_rbt = ft.RadioGroup(
            value="first best",
            content=ft.Row(
                controls=[
                    ft.Radio(value="first best", label="first best"),
                    ft.Radio(value="last best", label="last best"),
                ]
            ),
        )
        self.deleted_cb = ft.Checkbox(label="Show deleted")

        add_container = ft.Container(
            content=ft.FloatingActionButton(
                icon=ft.icons.ADD,
            ),
        )

        self.options_list = ft.Row(
            expand=True,
            controls=[
                add_container,
                ft.ListView(
                    expand=True,
                    controls=[
                        AnswerOptionCard(opt, "best") for opt in self.form_item.active
                    ],
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        self.controls = [
            ft.Row(
                controls=[self.back_bt, self.version_control],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            self.text_edit,
            self.description_edit,
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        controls=[
                            self.save_bt,
                            self.reverse_bt,
                            self.best_rbt,
                        ]
                    ),
                    self.deleted_cb,
                ],
            ),
            self.options_list,
        ]

    def save_click(self, *args):
        pass
