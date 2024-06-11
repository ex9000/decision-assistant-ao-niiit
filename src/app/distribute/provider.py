# singleton
from functools import partial
from itertools import starmap
from pathlib import Path

import numpy as np
import pandas as pd

from src.io import check_path
from src.lang import *
from .data_model import Supply, Target, Solution

__all__ = [
    "targets",
    "supplies",
    "solutions",
    "load_targets",
    "load_supplies",
    "save_targets",
    "save_supplies",
]

targets: list[Target] = []
supplies: list[Supply] = []
solutions: list[Solution] = []


def load_targets(file_path: str):
    global targets

    p = check_path(file_path)

    try:
        df = pd.read_excel(p)
        targets = list(starmap(Target, df.itertuples(index=False, name=None)))
    except Exception:
        raise Exception(E_CANNOT_PARSE_FILE.format(p.as_posix()).capitalize())


def load_supplies(file_path: str):
    global supplies

    p = check_path(file_path)

    try:
        df = pd.read_excel(p)
        supplies = list(starmap(Supply, df.itertuples(index=False, name=None)))
    except Exception:
        raise Exception(E_CANNOT_PARSE_FILE.format(p.as_posix()).capitalize())


def save_targets(file_path: str):
    targets.sort(key=lambda t: (not t.enabled, t.priority, t.name))
    try:
        if all(t.enabled for t in targets):
            df = pd.DataFrame(
                map(partial(Target.as_dict, exclude_enabled=True), targets)
            )
        else:
            df = pd.DataFrame(map(Target.as_dict, targets))

        df.to_excel(file_path, index=False)

    except Exception:
        p = Path(file_path).absolute()
        raise Exception(E_CANNOT_SAVE_FILE.format(p.as_posix()).capitalize())


def save_supplies(file_path: str):
    supplies.sort(key=lambda s: (not s.enabled, s.name))
    try:
        if all(s.enabled for s in supplies):
            df = pd.DataFrame(
                map(partial(Supply.as_dict, exclude_enabled=True), supplies)
            )
        else:
            df = pd.DataFrame(map(Supply.as_dict, supplies))

        df.to_excel(file_path, index=False)

    except Exception:
        p = Path(file_path).absolute()
        raise Exception(E_CANNOT_SAVE_FILE.format(p.as_posix()).capitalize())


def save_solutions(file_path: str):
    df = solution2df()
    try:
        df.to_excel(file_path, index=False)
    except Exception:
        p = Path(file_path).absolute()
        raise Exception(E_CANNOT_SAVE_FILE.format(p.as_posix()).capitalize())


def solution2df():
    unique = set(s for sol in solutions for s, _ in sol.used)
    used = sorted(unique, key=lambda s: s.name)
    total = np.zeros(len(used))
    data = np.full((len(solutions) + 2, len(used) + 1), np.nan, dtype=np.float64)
    for i, s in enumerate(solutions):
        price = 0
        for u, x in s.used:
            j = used.index(u)
            total[j] += x
            data[i, 1 + j] = x
            price += x * u.price
        data[i, 0] = price
    data[-2, 1:] = total
    data[-1, 0] = data[:, 0].sum()
    data[-1, 1:] = total * np.array([u.price for u in used])
    return pd.DataFrame(
        data=data,
        index=[t.name for t in targets]
              + [DISTRIBUTE.SOLUTION.K_TOTAL, DISTRIBUTE.SOLUTION.K_PRICE],
        columns=[DISTRIBUTE.SOLUTION.K_NAME, DISTRIBUTE.SOLUTION.K_PRICE]
                + [u.name for u in used],
    )
