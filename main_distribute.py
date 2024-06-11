import flet as ft

from src.app.common import on_theme_mode_switch_change
from src.app.distribute.gui.solution import build_solution_container
from src.app.distribute.gui.supply import build_supply_container
from src.app.distribute.gui.target import build_target_container
from src.lang import *


def window(page: ft.Page):
    switch_lang(Lang.RU)

    page.title = K_TACTICAL_PLANNING.capitalize()
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT

    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text(K_VIEW.capitalize()),
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Switch(
                            label_position=ft.LabelPosition.LEFT,
                            label=K_DARK_MODE.capitalize(),
                            value=page.theme_mode == ft.ThemeMode.DARK,
                            on_change=on_theme_mode_switch_change,
                        ),
                    )
                ],
            ),
        ],
    )

    supply = ft.Container()
    build_supply_container(supply)

    target = ft.Container()
    build_target_container(target)

    solve = ft.Container()
    build_solution_container(solve)

    tabs = ft.Tabs(
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                icon=ft.icons.WAREHOUSE,
                text=DISTRIBUTE.SUPPLY.K_FILE_NAME.capitalize(),
                content=supply,
            ),
            ft.Tab(
                icon=ft.icons.GPS_FIXED,
                text=DISTRIBUTE.TARGET.K_FILE_NAME.capitalize(),
                content=target,
            ),
            ft.Tab(
                icon=ft.icons.CHECKLIST,
                text=DISTRIBUTE.SOLUTION.K_FILE_NAME.capitalize(),
                content=solve,
            ),
        ],
    )

    page.add(
        ft.Row([menubar]),
        tabs,
    )
    page.update()


def main():
    ft.app(window)


if __name__ == "__main__":
    main()
