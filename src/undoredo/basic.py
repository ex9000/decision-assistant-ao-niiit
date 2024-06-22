from copy import copy
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from . import limit
from ..common import find_last_occurrence


@dataclass
class Version:
    counter: int
    obj: Any


class UndoRedo:
    def __init__(self, obj):
        self.pointer = -1
        self.versions: dict[datetime, Version] = {}
        self.history: list[datetime] = []

        self._create_version(obj)

    def get_obj(self):
        tm = self.history[self.pointer]
        return self.versions[tm].obj

    def commit(self, obj, duplicate_check=True):
        if duplicate_check and obj == self.get_obj():
            return

        self._fix_undo()
        self._create_version(obj)
        self._fix_history()

    def undo(self):
        if self.pointer > 0:
            self.pointer -= 1

    def redo(self):
        if self._has_redo():
            self.pointer += 1

    def rollback(self, tm: datetime):
        self.pointer = find_last_occurrence(tm, self.history)

    def snapshots(self) -> list[datetime]:
        return sorted(self.versions.keys(), reverse=True)

    def _has_redo(self):
        return self.pointer < len(self.history) - 1

    def _fix_history(self):
        if len(self.history) > 2 * limit.LIMIT:
            for tm in self.history[: limit.LIMIT]:
                self.versions[tm].counter -= 1
                if self.versions[tm].counter == 0:
                    del self.versions[tm]
            self.history = self.history[limit.LIMIT:]
            self.pointer -= limit.LIMIT

    def _create_version(self, obj):
        tm = datetime.now()
        self.versions[tm] = Version(1, copy(obj))
        self.history.append(tm)
        self.pointer += 1

    def _fix_undo(self):
        if self._has_redo():
            tm = self.history[self.pointer]
            self.history.append(tm)
            self.versions[tm].counter += 1
            self.pointer = len(self.history) - 1
