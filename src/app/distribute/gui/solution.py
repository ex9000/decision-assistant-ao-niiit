import flet as ft

import src.app.distribute.provider as provider
from src.app.common import ALLOWED_EXCEL_EXTS
from src.app.distribute.data_model import Solution
from src.app.distribute.logic import bin_search_solution
from src.lang import *


def build_solution_container(c: ft.Container):
    def on_saved_file(r: ft.FilePickerResultEvent):
        if not r.path:
            return

        p = r.path
        if not p.endswith(".xlsx"):
            p += ".xlsx"
        provider.save_solutions(p)

        c.page.dialog = ft.AlertDialog(title=ft.Text(K_DATA_SAVED.capitalize()))
        c.page.dialog.open = True
        c.page.update()

    def on_solve():
        provider.solutions: list[Solution] = bin_search_solution()
        list_view.controls.clear()

        for s in provider.solutions:
            if not s.used:
                continue
            card = ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        [ft.Text(s.target.name)]
                        + [
                            ft.Chip(
                                label=ft.Text(f"{u.name} x{x:0.2f}"),
                                color=ft.colors.ERROR_CONTAINER,
                                on_click=lambda _: None,
                            )
                            for u, x in s.used
                        ]
                    )
                )
            )
            card.content.padding = 5
            list_view.controls.append(card)
        list_view.update()

    list_view = ft.ListView(
        expand=True,
    )

    solve_button = ft.TextButton(
        icon=ft.icons.FIND_REPLACE,
        text=K_FIND_SOLUTION.capitalize(),
        on_click=lambda _: on_solve(),
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
            controls=[solve_button, save, save_picker],
        )
    )
    buttons_row.margin = 5

    c.content = ft.Column(
        controls=[
            buttons_row,
            ft.Divider(),
            list_view,
        ],
    )
