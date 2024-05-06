def solve(a, b, c):
    """a x^2 + bx + c = 0"""
    if a < 0:
        a, b, c = -a, -b, -c

    d = (b**2 - 4 * a * c) ** 0.5

    return (-b - d) / (2 * a), (-b + d) / (2 * a)
