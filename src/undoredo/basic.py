from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from . import limit


class UndoRedoBase:
    undoredo_tm = None

    def __init__(self):
        self.undoredo_tm: datetime | None = None


@dataclass
class Version:
    counter: int
    obj: Any


class UndoRedoHolder:
    def __init__(self, obj: UndoRedoBase):
        self.pointer = -1
        self.versions: dict[datetime, Version] = {}
        self.history: list[datetime] = []

        self._create_version(obj)

    def get_obj(self):
        tm = self.get_tm()
        return self.versions[tm].obj

    def get_tm(self):
        return self.history[self.pointer]

    def commit(self, obj: UndoRedoBase, duplicate_check=True):
        if duplicate_check and obj == self.get_obj():
            return

        self._commit(obj)

    def has_undo(self):
        return self.pointer > 0

    def has_redo(self):
        return self.pointer < len(self.history) - 1

    def undo(self):
        if self.has_undo():
            self.pointer -= 1

    def redo(self):
        if self.has_redo():
            self.pointer += 1

    def rollback(self, tm: datetime):
        self.pointer = self.history.index(tm)

    def snapshots(self) -> list[datetime]:
        return sorted(self.versions.keys(), reverse=True)

    def validate(self, obj: UndoRedoBase):
        # versions are the same
        if obj.undoredo_tm == self.history[self.pointer]:
            return

        # rollback to required version
        if obj.undoredo_tm in self.versions:
            self.pointer = self.history.index(obj.undoredo_tm)
            return

        # commit as new one
        self._commit(obj, obj.undoredo_tm)

    def _commit(self, obj: UndoRedoBase, tm: datetime = None):
        self._fix_undo()
        self._create_version(obj, tm=tm)
        self._fix_history()

    def _fix_history(self):
        if len(self.history) > 2 * limit.LIMIT:
            for tm in self.history[: limit.LIMIT]:
                self.versions[tm].counter -= 1
                if self.versions[tm].counter == 0:
                    del self.versions[tm]

            self.history = self.history[limit.LIMIT :]
            self.pointer -= limit.LIMIT

    def _create_version(self, obj: UndoRedoBase, tm: datetime = None):
        if tm is None:
            tm = datetime.now()

        # update tm
        obj.undoredo_tm = tm

        self.versions[tm] = Version(1, deepcopy(obj))
        self.history.append(tm)
        self.pointer += 1

    def _fix_undo(self):
        if self.has_redo():
            tm = self.get_tm()
            self.history.append(tm)
            self.versions[tm].counter += 1
            self.pointer = len(self.history) - 1
