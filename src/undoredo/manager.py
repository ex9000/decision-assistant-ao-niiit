from datetime import datetime
from typing import Any

from src.common import identity, assign
from .basic import UndoRedo

entities: dict[Any, UndoRedo] = {}


def commit(obj, key=identity, duplicate_check=True):
    return _new_or_do(
        obj, key, lambda k: entities[k].commit(obj, duplicate_check=duplicate_check)
    )


def undo(obj, key=identity):
    def _internal(k):
        entities[k].undo()
        assign(obj, entities[k].get_obj())

    return _new_or_do(obj, key, _internal)


def redo(obj, key=identity):
    def _internal(k):
        entities[k].redo()
        assign(obj, entities[k].get_obj())

    return _new_or_do(obj, key, _internal)


def rollback(obj, tm: datetime, key=identity):
    def _internal(k):
        entities[k].rollback(tm)
        assign(obj, entities[k].get_obj())

    return _new_or_do(obj, key, _internal)


def snapshots(obj, key=identity):
    return _new_or_do(obj, key, lambda k: entities[k].snapshots())


def _new_or_do(obj, key, action):
    global entities

    k = key(obj)
    if k not in entities:
        entities[k] = UndoRedo(obj)
    else:
        return action(k)
