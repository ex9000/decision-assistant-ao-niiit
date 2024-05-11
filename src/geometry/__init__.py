import numpy as np


def get_line(x1, y1, x2, y2):
    a = np.array([[x1, y1, 1], [x2, y2, 1], [1, 1, 1]])
    b = np.array([0, 0, 1])
    a, b, c = np.linalg.solve(a, b)
    return a, b, c


def intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    """Two lines: (x1, y1, x2, y2) and (x3, y3, x4, y4)"""

    a1, b1, c1 = get_line(x1, y1, x2, y2)
    a2, b2, c2 = get_line(x3, y3, x4, y4)

    a = np.array([[a1, b1], [a2, b2]])
    b = np.array([-c1, -c2])
    x, y = np.linalg.solve(a, b)
    return x, y


def cart2pol(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho


def pol2cart(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y
