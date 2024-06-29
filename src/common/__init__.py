from itertools import chain, combinations

number = int | float


def nop(*args, **kwargs):
    pass


def identity(x):
    return x


def assign(left, right):
    for k, v in vars(right).items():
        setattr(left, k, v)


def find_last_occurrence[T](x: T, xs: list[T]):
    return len(xs) - 1 - xs[::-1].index(x)


def subsets(size, smallest=0, biggest=None):
    if biggest is None:
        biggest = size
    return chain(
        *map(lambda i: combinations(range(size), i), range(smallest, biggest + 1))
    )
