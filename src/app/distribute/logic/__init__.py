import numpy as np
import scipy as sp

from src.app.distribute.data_model import Solution
from src.app.distribute.provider import supplies, targets


def bin_search_solution() -> list:
    l, r = 0, sum(t.enabled for t in targets) + 1
    accepted = []

    while r - l > 1:
        if new := solve(mid := (l + r) // 2):
            l, accepted = mid, new
        else:
            r = mid

    return accepted


def solve(targets_amount: int) -> list:
    ts = [t for t in targets if t.enabled][:targets_amount]
    ss = [s for s in supplies if s.enabled]
    n = len(ss)
    k = len(ts)

    c = np.array([s.price for s in ss] * targets_amount)

    b_ub = np.array([s.amount for s in ss] + [-1] * k)
    a_ub = np.zeros((n + k, n * k))
    for i in range(n):
        a_ub[i, i * k: (i + 1) * k] = 1
    for i in range(k):
        a_ub[i + n, i::k] = -1

    potential = np.array([s.potential for s in ss])
    b_eq = np.array([t.health for t in ts])
    a_eq = np.zeros((k, n * k))
    for i in range(k):
        a_eq[i, i::k] = potential

    solution = sp.optimize.linprog(c, a_ub, b_ub, a_eq, b_eq)

    if not solution.success:
        return None

    v = solution.x
    return [
        Solution(
            target=t,
            used=[(ss[j], x) for j, x in enumerate(v[i * k: (i + 1) * k]) if x > 0],
        )
        for i, t in enumerate(ts)
    ]
