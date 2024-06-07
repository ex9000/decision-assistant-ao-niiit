import flet as ft

import src.app.distribute.provider as provider
from src.app.common import ALLOWED_EXCEL_EXTS
from src.app.distribute.data_model import Target
from src.lang import *

target_counter = 0


def add_target_card(t: Target, lv: ft.ListView):
    def switch_enabled(enabled: bool):
        t.enabled = enabled

    def change_name(name: str):
        t.name = name

    def change_health(health: float):
        t.health = health

    def change_priority(priority: int):
        t.priority = priority

    def remove():
        lv.controls.remove(card)
        provider.targets.remove(t)
        lv.update()

    card = ft.Card(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Switch(
                    value=t.enabled,
                    on_change=lambda e: switch_enabled(e.control.value),
                ),
                ft.TextField(
                    value=t.name,
                    hint_text=DISTRIBUTE.TARGET.K_NAME.capitalize(),
                    tooltip=DISTRIBUTE.TARGET.K_NAME.capitalize(),
                    on_change=lambda e: change_name(e.control.value),
                ),
                ft.TextField(
                    value=str(t.health),
                    width=200,
                    icon=ft.icons.SHIELD,
                    hint_text=DISTRIBUTE.TARGET.K_HEALTH.capitalize(),
                    tooltip=DISTRIBUTE.TARGET.K_HEALTH.capitalize(),
                    input_filter=ft.InputFilter(r"^[0-9]*\.?[0-9]*$"),
                    on_change=lambda e: change_health(float(e.control.value or "0")),
                ),
                ft.TextField(
                    value=str(t.priority),
                    width=200,
                    icon=ft.icons.FILTER_LIST,
                    hint_text=DISTRIBUTE.TARGET.K_PRIORITY.capitalize(),
                    tooltip=DISTRIBUTE.TARGET.K_PRIORITY.capitalize(),
                    input_filter=ft.InputFilter(r"^[0-9]*$"),
                    on_change=lambda e: change_priority(int(e.control.value or "0")),
                ),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: remove()),
            ],
        )
    )

    lv.controls.append(card)
    lv.update()


def build_target_container(c: ft.Container):
    def new_target(t: Target = None):
        global target_counter
        if t is None:
            target_counter += 1
            t = Target(K_TARGET.capitalize() + f" {target_counter}", 100, 1)
            provider.targets.append(t)
        add_target_card(t, list_view)

    def on_picked_file(r: ft.FilePickerResultEvent):
        if not r.files:
            return

        provider.load_targets(r.files[0].path)

        list_view.controls.clear()
        for t in provider.targets:
            new_target(t)

        c.page.dialog = ft.AlertDialog(title=ft.Text(K_DATA_LOADED.capitalize()))
        c.page.dialog.open = True
        c.page.update()

    def on_saved_file(r: ft.FilePickerResultEvent):
        if not r.path:
            return

        p = r.path
        if not p.endswith(".xlsx"):
            p += ".xlsx"
        provider.save_targets(p)

        c.page.dialog = ft.AlertDialog(title=ft.Text(K_DATA_SAVED.capitalize()))
        c.page.dialog.open = True
        c.page.update()

    list_view = ft.ListView(
        expand=True,
    )

    load_picker = ft.FilePicker(on_result=on_picked_file)
    load = ft.TextButton(
        icon=ft.icons.TABLE_VIEW,
        text=K_LOAD_FROM_FILE.capitalize(),
        on_click=lambda _: load_picker.pick_files(
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=ALLOWED_EXCEL_EXTS,
        ),
    )

    save_picker = ft.FilePicker(on_result=on_saved_file)
    save = ft.TextButton(
        icon=ft.icons.SIM_CARD_DOWNLOAD,
        text=K_SAVE_TO_FILE.capitalize(),
        on_click=lambda _: save_picker.save_file(
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=ALLOWED_EXCEL_EXTS,
        ),
    )

    buttons_row = ft.Container(
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[load, save, load_picker, save_picker],
        )
    )
    buttons_row.margin = 5

    add_container = ft.Container(
        content=ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=lambda e: new_target(),
        ),
    )
    add_container.margin = 5
    c.content = ft.Column(
        controls=[
            buttons_row,
            ft.Divider(),
            ft.Row(
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    add_container,
                    list_view,
                ],
            ),
        ],
    )
