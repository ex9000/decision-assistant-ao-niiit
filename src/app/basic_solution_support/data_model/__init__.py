from dataclasses import dataclass, field
from random import randint


@dataclass(frozen=False)
class Item:
    name: str
    usefulness: int = field(default_factory=lambda: randint(0, 3))
    precision: int = field(default_factory=lambda: randint(0, 3))


FUZZY_WIDTH = 1
PRECISION_VALUES = [1.0, 0.7, 0.4, 0.1]
