from datetime import datetime
from typing import Any

from src.common import identity, assign
from .basic import UndoRedoHolder, UndoRedoBase

entities: dict[Any, UndoRedoHolder] = {}


def commit(obj: UndoRedoBase, key=identity, duplicate_check=True):
    return _new_or_do(
        obj, key, lambda k: entities[k].commit(obj, duplicate_check=duplicate_check)
    )


def undo(obj: UndoRedoBase, key=identity):
    def _internal(k):
        entities[k].undo()
        assign(obj, entities[k].get_obj())

    return _new_or_do(obj, key, _internal)


def redo(obj: UndoRedoBase, key=identity):
    def _internal(k):
        entities[k].redo()
        assign(obj, entities[k].get_obj())

    return _new_or_do(obj, key, _internal)


def has_undo(obj: UndoRedoBase, key=identity):
    return _new_or_do(obj, key, lambda k: entities[k].has_undo()) or False


def has_redo(obj: UndoRedoBase, key=identity):
    return _new_or_do(obj, key, lambda k: entities[k].has_redo()) or False


def rollback(obj: UndoRedoBase, tm: datetime, key=identity):
    def _internal(k):
        entities[k].rollback(tm)
        assign(obj, entities[k].get_obj())

    return _new_or_do(obj, key, _internal)


def snapshots(obj: UndoRedoBase, key=identity):
    return _new_or_do(obj, key, lambda k: entities[k].snapshots()) or [obj.undoredo_tm]


def get_tm(obj: UndoRedoBase, key=identity):
    return _new_or_do(obj, key, lambda k: entities[k].get_tm()) or obj.undoredo_tm


def _new_or_do(obj: UndoRedoBase, key, action):
    global entities

    k = key(obj)
    if k not in entities:
        entities[k] = UndoRedoHolder(obj)
    else:
        entities[k].validate(obj)
        return action(k)
