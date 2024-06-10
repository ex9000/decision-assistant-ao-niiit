import flet as ft

from src.app.common import on_theme_mode_switch_change
from src.lang import *


def window(page: ft.Page):
    switch_lang(Lang.RU)

    page.title = K_TACTICAL_PLANNING
    page.theme_mode = ft.ThemeMode.LIGHT

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

    tabs = ft.Tabs(
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                icon=ft.icons.WAREHOUSE,
                text=DISTRIBUTE.SUPPLY.K_FILE_NAME.capitalize(),
                content=ft.Container(
                    content=ft.Image(
                        "./images/item.png", fit=ft.ImageFit.FIT_HEIGHT, height=200
                    ),
                    alignment=ft.alignment.center,
                ),
            ),
            ft.Tab(
                icon=ft.icons.GPS_FIXED,
                text=DISTRIBUTE.TARGET.K_FILE_NAME.capitalize(),
                content=ft.Container(
                    content=ft.Image(
                        "./images/item.png", fit=ft.ImageFit.FIT_HEIGHT, height=200
                    ),
                    alignment=ft.alignment.center,
                ),
            ),
            ft.Tab(
                icon=ft.icons.CHECKLIST,
                text=DISTRIBUTE.SOLUTION.K_FILE_NAME.capitalize(),
                content=ft.Container(
                    content=ft.Image(
                        "./images/item.png", fit=ft.ImageFit.FIT_HEIGHT, height=200
                    ),
                    alignment=ft.alignment.center,
                ),
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
