import numpy as np
import scipy as sp
from numpy.polynomial.polynomial import polyval


def solve_matrix(matrix: np.ndarray, sum_constraint: float = 1) -> np.ndarray:
    """Solve Lagrangian, last 2 rows and 2 columns of matrix is extra lambda coefficients"""

    assert len(matrix.shape) == 2

    h, w = matrix.shape
    assert h == w

    vector = np.zeros((h, 2))
    vector[-1, 0] = sum_constraint
    vector[-2, 1] = 1

    solution = sp.linalg.solve(matrix, vector, assume_a="sym")[-2:, ...].T

    assert (solution[1] > 0).any(), "at least one share must be increasing"
    assert (solution[1] < 0).any(), "at least one share must be decreasing"

    return solution


def apply_gt_constraints(
        solution: np.ndarray, constraints: np.ndarray
) -> ((float, float), (int, int)):
    """Finds allowed segment and critical variable indices"""

    assert constraints.ndim == 1
    assert solution.ndim == 2
    h, w = solution.shape

    assert h == 2 and w == len(constraints)

    critical = (constraints + solution[0]) / solution[1]

    low = critical[solution[1] > 0].max()
    high = critical[solution[1] < 0].min()

    low_id = (polyval(low, solution) - constraints).argmin()
    high_id = (polyval(high, solution) - constraints).argmin()

    return (low, high), (low_id, high_id)


def apply_lt_constraints(
        solution: np.ndarray, constraints: np.ndarray
) -> ((float, float), (int, int)):
    """Finds allowed segment and critical variable indices"""

    # inverse inequalities
    return apply_gt_constraints(-solution, -constraints)


def lowest_parabola_point(matrix: np.ndarray, solution: np.ndarray) -> (float, float):
    """Finds the lowest parabola point - return and variance.

    Args:
        matrix (np.ndarray): The matrix representing the quadratic form.
        solution (np.ndarray): The solution vector.

    Returns:
        (float, float): The return value 'r' and the variance 'v'.
    """

    m = matrix
    s = solution

    # d<Ax, x> = 2<Ax, dx>, if A == A.T
    # A := m, x := s(r)
    # d(s(r)) = s[1], because s(r) === s[0] + s[1] * r
    # 2<Ax, dx> = 2 <m s, s[1]> = 2 * s @ m @ s[1] = [c, k]
    c, k = s @ m @ s[1]  # do not multiply on `2` because 2(kr+c)=0 <==> kr+c=0

    # 2 * s @ m @ s[1] = 0 --> k * r + c = 0
    # k * r = -c ==> r = -c / k
    r = -c / k
    w = polyval(r, s)
    v = w @ m @ w

    # return and variance
    return r, v


def quadratic_form(matrix: np.ndarray, weights: np.ndarray) -> np.ndarray:
    m = matrix
    xs = weights

    # The np.einsum function is a powerful tool in NumPy that allows for explicit specification
    # of the indices of the input and output arrays, enabling complex operations like the
    # quadratic form to be computed in a concise and efficient manner. In the
    # expression, 'ij,jk,ik->i' specifies the pattern of multiplication and
    # summation: for each vector i in xs, multiply with matrix m and the same vector i, and
    # sum over the indices j and k to get the quadratic form.
    #
    # This approach is efficient and takes advantage of NumPy's optimized performance for array
    # operations. If you have a large number of vectors, this method will be much faster than
    # computing each quadratic form in a loop.

    return np.einsum("ij,jk,ik->i", xs, m, xs, optimize=True)


def frontier_derivation(
        xs: np.ndarray, matrix: np.ndarray, solution: np.ndarray
) -> np.ndarray:
    """
    Computes the derivative of the quadratic form.
    It is defined by the matrix 'matrix' and the 'solution' vectors.

    Parameters:
        xs (np.ndarray): Points at which to evaluate the derivatives.
        matrix (np.ndarray): The matrix defining the quadratic form.
        solution (np.ndarray): A 2xN matrix representing N solution vectors.

    Returns:
    np.ndarray: An array of the derivatives of the quadratic form evaluated at each point in 'xs'.
    """
    m = matrix
    s = solution

    poly = 2 * (s @ m @ s[1])
    return polyval(xs, poly)


def make_covariance(dispersion: np.ndarray, correlation: np.ndarray) -> np.ndarray:
    std = dispersion ** 0.5
    return correlation * std * std.T
