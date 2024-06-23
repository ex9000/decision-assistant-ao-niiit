from typing import Callable

import flet as ft

from src.common import nop
from src.lang import *
from src.undoredo import UndoRedoProtocol


class VersionControl[T: UndoRedoProtocol](ft.Row):
    def __init__(self, undoredo: T, callback: Callable[[], None] = nop):
        super().__init__()
        self.undoredo = undoredo
        self.callback = callback

        self.prev = ft.TextButton(
            icon=ft.icons.UNDO,
            text=K_OLDER.capitalize(),
            on_click=self.click_prev,
        )
        self.versions = ft.Dropdown(value="actual", on_change=self.select_snapshot)
        self.next = ft.TextButton(
            content=ft.Row(
                [ft.Text(K_NEWER.capitalize()), ft.Icon(name=ft.icons.REDO)]
            ),
            on_click=self.click_next,
        )

        self.controls = [
            ft.Text(
                K_VERSION.capitalize() + ":",
                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            ),
            self.versions,
            self.prev,
            self.next,
        ]

    def click_prev(self, *_):
        self.undoredo.undo()
        self.update()

        self.callback()

    def click_next(self, *_):
        self.undoredo.redo()
        self.update()

        self.callback()

    def select_snapshot(self, *_):
        snapshots = list(map(str, self.undoredo.snapshots()))
        p = snapshots.index(self.versions.value)
        tm = self.undoredo.snapshots()[p]
        self.undoredo.rollback(tm)
        self.update()

        self.callback()

    def before_update(self):
        self.versions.options = [
            ft.dropdown.Option(key=str(tm), text=str(tm))
            for tm in self.undoredo.snapshots()
        ]
        self.versions.value = str(self.undoredo.get_tm())

        self.prev.disabled = not self.undoredo.has_undo()
        self.next.disabled = not self.undoredo.has_redo()
