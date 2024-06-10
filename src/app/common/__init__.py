import flet as ft


def on_theme_mode_switch_change(e: ft.ControlEvent):
    if e.control.value:
        on_theme_mode_change(ft.ThemeMode.DARK, e.page)
    else:
        on_theme_mode_change(ft.ThemeMode.LIGHT, e.page)


def on_theme_mode_change(theme_mode: ft.ThemeMode, page: ft.Page):
    page.theme_mode = theme_mode
    page.update()
