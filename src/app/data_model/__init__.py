from dataclasses import dataclass


@dataclass
class Item:
    name: str
    usefulness: int
    precision: int


FUZZY_WIDTH = 1
PRECISION_VALUES = [1.0, 0.7, 0.4, 0.1]
