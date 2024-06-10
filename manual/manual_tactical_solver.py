from dataclasses import dataclass
from itertools import starmap
from pprint import pp

import numpy as np
import scipy as sp


@dataclass
class Supply:
    name: str
    potential: float
    amount: int
    price: float


@dataclass
class Target:
    name: str
    health: float
    priority: int


supply = list(
    starmap(
        Supply,
        [
            ("Пехотинец", 0.01, 10 ** 4, 1000),
            ("Танк", 2, 50, 10 ** 6),
            ("Артилерия", 10, 5, 5 * 10 ** 6),
            ("Авиация", 20, 10, 10 ** 8),
        ],
    )
)

targets = list(
    starmap(
        Target,
        [
            ("Генштаб", 200, 1),
            ("Склады", 20, 2),
            ("Электростанция", 30, 2),
            ("Боевой взвод", 2, 3),
        ],
    )
)

targets.sort(key=lambda tgt: (tgt.priority, tgt.health))

pp(supply)
pp(targets)

# rough
total = 0
for s in supply:
    total += s.potential * s.amount

left = total
covered = 0
for t in targets:
    if t.health > left:
        break
    covered += 1
    left -= t.health

print("Got", covered, "targets of", len(targets))
print("Used", f"{((total - left) / total):.2%}", "of total potential")

targets = targets[:covered]

n = len(supply)
k = len(targets)

c = np.array([s.price for s in supply] * covered)

b_ub = np.array([s.amount for s in supply] + [-1] * k)
a_ub = np.zeros((n + k, n * k))
for i in range(n):
    a_ub[i, i * k: (i + 1) * k] = 1
for i in range(k):
    a_ub[i + n, i::k] = -1

potential = np.array([s.potential for s in supply])
b_eq = np.array([t.health for t in targets])
a_eq = np.zeros((k, n * k))
for i in range(k):
    a_eq[i, i::k] = potential

print(c.round(2))
print(b_ub.round(2))
print(a_ub.round(2))
print(b_eq.round(2))
print(a_eq.round(2))

solution = sp.optimize.linprog(c, a_ub, b_ub, a_eq, b_eq)
print()

if not solution.success:
    print("Optimization failed")
    quit()

x = solution.x
print("Total price:", c @ x)
for i, t in enumerate(targets):
    print()
    print(f"{t.name} ({t.health})", ":")
    for j, s in enumerate(supply):
        amount = x[i::k][j]
        if np.isclose(amount, 0):
            continue
        print(f"\t{s.name} ({s.potential}): x{amount}")
