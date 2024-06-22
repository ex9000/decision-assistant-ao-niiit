from datetime import datetime
from typing import overload, Protocol, Callable, TYPE_CHECKING

from src.common import identity
from . import manager


class UndoRedoProtocol(Protocol):
    def undo(self): ...

    def redo(self): ...

    def commit(self): ...

    def rollback(self, tm: datetime): ...

    def snapshots(self) -> list[datetime]: ...


@overload
def undoredo[T](cls) -> UndoRedoProtocol | T: ...


@overload
def undoredo[
T
](*, key=identity, duplicate_check=True) -> Callable[[T], UndoRedoProtocol | T]: ...


def undoredo(cls=None, *, key=identity, duplicate_check=True):
    if cls is None:
        # noinspection PyArgumentList
        return lambda clazz: undoredo(clazz, key=key, duplicate_check=duplicate_check)

    if TYPE_CHECKING:  # tweak
        return type(cls.__name__, (UndoRedoProtocol, cls), {})

    setattr(
        cls,
        "commit",
        lambda self: manager.commit(self, key=key, duplicate_check=duplicate_check),
    )

    setattr(cls, "undo", lambda self: manager.undo(self, key=key))
    setattr(cls, "redo", lambda self: manager.redo(self, key=key))
    setattr(cls, "snapshots", lambda self: manager.snapshots(self, key=key))
    setattr(cls, "rollback", lambda self, tm: manager.rollback(self, tm, key=key))

    return cls
