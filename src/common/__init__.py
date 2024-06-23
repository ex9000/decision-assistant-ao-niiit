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
