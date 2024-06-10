from dataclasses import dataclass

from src.lang import DISTRIBUTE


@dataclass(frozen=True)
class Supply:
    name: str
    potential: float
    amount: int
    price: float
    enabled: bool = True

    def as_dict(self, exclude_enabled=False):
        d = {
            DISTRIBUTE.SUPPLY.K_NAME: self.name,
            DISTRIBUTE.SUPPLY.K_POTENTIAL: self.potential,
            DISTRIBUTE.SUPPLY.K_AMOUNT: self.amount,
            DISTRIBUTE.SUPPLY.K_PRICE: self.price,
            DISTRIBUTE.SUPPLY.K_ACTIVE: self.enabled,
        }
        if not exclude_enabled:
            d[DISTRIBUTE.SUPPLY.K_ACTIVE] = self.enabled
        return d


@dataclass(frozen=True)
class Target:
    name: str
    health: float
    priority: int
    enabled: bool = True

    def as_dict(self, exclude_enabled=False):
        d = {
            DISTRIBUTE.TARGET.K_NAME: self.name,
            DISTRIBUTE.TARGET.K_HEALTH: self.health,
            DISTRIBUTE.TARGET.K_PRIORITY: self.priority,
            DISTRIBUTE.TARGET.K_ACTIVE: self.enabled,
        }
        if not exclude_enabled:
            d[DISTRIBUTE.TARGET.K_ACTIVE] = self.enabled
        return d


@dataclass
class Solution:
    target: Target
    used: list[tuple[Supply, float]]
