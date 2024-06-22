from tqdm import tqdm


def find_last_occurrence[T](x: T, xs: list[T]):
    return len(xs) - 1 - xs[::-1].index(x)


def main():
    xs = list(range(5 * 10 ** 7))
    # ys = list(reversed(xs))

    # print(ys.index(2))
    s = 0
    for i in tqdm(range(10)):
        s += find_last_occurrence(i, xs)
    print(s)


if __name__ == "__main__":
    main()
