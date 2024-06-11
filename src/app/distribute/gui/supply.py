import flet as ft

import src.app.distribute.provider as provider
from src.app.common import ALLOWED_EXCEL_EXTS
from src.app.distribute.data_model import Supply
from src.lang import *

weapon_counter = 0


def add_supply_card(s: Supply, lv: ft.ListView):
    def switch_enabled(enabled: bool):
        s.enabled = enabled

    def change_name(name: str):
        s.name = name

    def change_potential(potential: float):
        s.potential = potential

    def change_amount(amount: int):
        s.amount = amount

    def change_price(price: float):
        s.price = price

    def remove():
        lv.controls.remove(card)
        provider.supplies.remove(s)
        lv.update()

    card = ft.Card(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Switch(
                    value=s.enabled,
                    on_change=lambda e: switch_enabled(e.control.value),
                ),
                ft.TextField(
                    value=s.name,
                    hint_text=DISTRIBUTE.SUPPLY.K_NAME.capitalize(),
                    tooltip=DISTRIBUTE.SUPPLY.K_NAME.capitalize(),
                    on_change=lambda e: change_name(e.control.value),
                ),
                ft.TextField(
                    value=str(s.potential),
                    width=200,
                    icon=ft.icons.ROCKET_LAUNCH,
                    hint_text=DISTRIBUTE.SUPPLY.K_POTENTIAL.capitalize(),
                    tooltip=DISTRIBUTE.SUPPLY.K_POTENTIAL.capitalize(),
                    input_filter=ft.InputFilter(r"^[0-9]*\.?[0-9]*$"),
                    on_change=lambda e: change_potential(float(e.control.value or "0")),
                ),
                ft.TextField(
                    value=str(s.amount),
                    width=200,
                    icon=ft.icons.DATASET,
                    hint_text=DISTRIBUTE.SUPPLY.K_AMOUNT.capitalize(),
                    tooltip=DISTRIBUTE.SUPPLY.K_AMOUNT.capitalize(),
                    input_filter=ft.InputFilter(r"^[0-9]*$"),
                    on_change=lambda e: change_amount(int(e.control.value or "0")),
                ),
                ft.TextField(
                    value=str(s.price),
                    width=200,
                    icon=ft.icons.MONEY,
                    hint_text=DISTRIBUTE.SUPPLY.K_PRICE.capitalize(),
                    tooltip=DISTRIBUTE.SUPPLY.K_PRICE.capitalize(),
                    input_filter=ft.InputFilter(r"^[0-9]*\.?[0-9]*$"),
                    on_change=lambda e: change_price(float(e.control.value or "0")),
                ),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: remove()),
            ],
        )
    )

    lv.controls.append(card)
    lv.update()


def build_supply_container(c: ft.Container):
    def new_supply(s: Supply = None):
        global weapon_counter
        weapon_counter += 1
        if s is None:
            s = Supply(K_WEAPON.capitalize() + f" {weapon_counter}", 2.5, 10, 1.05)
            provider.supplies.append(s)
        add_supply_card(s, list_view)

    def on_picked_file(r: ft.FilePickerResultEvent):
        if not r.files:
            return

        provider.load_supplies(r.files[0].path)

        list_view.controls.clear()
        for s in provider.supplies:
            new_supply(s)

        c.page.dialog = ft.AlertDialog(title=ft.Text(K_DATA_LOADED.capitalize()))
        c.page.dialog.open = True
        c.page.update()

    def on_saved_file(r: ft.FilePickerResultEvent):
        if not r.path:
            return

        provider.save_supplies(r.path)

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
            on_click=lambda e: new_supply(),
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
