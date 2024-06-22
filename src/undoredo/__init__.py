from datetime import datetime
from typing import Protocol, Type

from src.common import identity
from . import manager
from .basic import UndoRedoBase


class UndoRedoProtocol(Protocol):
    def has_undo(self) -> bool: ...

    def has_redo(self) -> bool: ...

    def undo(self): ...

    def redo(self): ...

    def commit(self): ...

    def rollback(self, tm: datetime): ...

    def snapshots(self) -> list[datetime]: ...


def undoredo(key=identity, duplicate_check=True) -> Type[UndoRedoProtocol]:
    class _InnerUndoRedo(UndoRedoBase):
        def has_undo(self) -> bool:
            return manager.has_undo(self, key=key)

        def has_redo(self) -> bool:
            return manager.has_undo(self, key=key)

        def undo(self):
            return manager.undo(self, key=key)

        def redo(self):
            return manager.redo(self, key=key)

        def commit(self):
            return manager.commit(self, key=key, duplicate_check=duplicate_check)

        def rollback(self, tm: datetime):
            return manager.rollback(self, tm, key=key)

        def snapshots(self) -> list[datetime]:
            return manager.snapshots(self, key=key)

    return _InnerUndoRedo
