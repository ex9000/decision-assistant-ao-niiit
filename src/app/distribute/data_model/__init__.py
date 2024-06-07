from dataclasses import dataclass, field
from uuid import uuid4

from src.lang import DISTRIBUTE


@dataclass(unsafe_hash=True)
class Supply:
    name: str = field(compare=False)
    potential: float = field(compare=False)
    amount: int = field(compare=False)
    price: float = field(compare=False)
    enabled: bool = field(default=True, compare=False)
    _id: str = field(default_factory=uuid4)

    def as_dict(self, exclude_enabled=False):
        d = {
            DISTRIBUTE.SUPPLY.K_NAME.capitalize(): self.name,
            DISTRIBUTE.SUPPLY.K_POTENTIAL.capitalize(): self.potential,
            DISTRIBUTE.SUPPLY.K_AMOUNT.capitalize(): self.amount,
            DISTRIBUTE.SUPPLY.K_PRICE.capitalize(): self.price,
        }
        if not exclude_enabled:
            d[DISTRIBUTE.SUPPLY.K_ACTIVE.capitalize()] = self.enabled
        return d


@dataclass(unsafe_hash=True)
class Target:
    name: str = field(compare=False)
    health: float = field(compare=False)
    priority: int = field(compare=False)
    enabled: bool = field(default=True, compare=False)
    _id: str = field(default_factory=uuid4)

    def as_dict(self, exclude_enabled=False):
        d = {
            DISTRIBUTE.TARGET.K_NAME.capitalize(): self.name,
            DISTRIBUTE.TARGET.K_HEALTH.capitalize(): self.health,
            DISTRIBUTE.TARGET.K_PRIORITY.capitalize(): self.priority,
        }
        if not exclude_enabled:
            d[DISTRIBUTE.TARGET.K_ACTIVE.capitalize()] = self.enabled
        return d


@dataclass
class Solution:
    target: Target
    used: list[tuple[Supply, float]]
