"""solutions produced with sympy /jupyter_sketches/fit_ssr.ipynb"""

import numpy as np


@np.vectorize
def fit_center_pm_offsets(x, y, z, vx, vy, vz):
    """
    Triangular Fuzzy-Random value described like:
    - center = `y`
    - left = `y-x`
    - right = `y+z`

    Shift-Scale Representation based on Normal `shift` and `scale`
    with Symmetric Triangular value Tr(`mode`, 1)
    """
    shift = (
        (1 / 12)
        * (-vx * x + 12 * vx * y + 7 * vx * z - 7 * vz * x + 12 * vz * y + vz * z)
        / (vx + vz)
    )
    scale = x + z
    var_shift = (
        (1 / 8)
        * (-(vx**2) + 8 * vx * vy + 2 * vx * vz + 8 * vy * vz - vz**2)
        / (vx + vz)
    )
    var_scale = 2 * vx + 2 * vz
    mode = (-vx + vz) / (4 * vx + 4 * vz)
    return [
        shift,
        scale,
        var_shift,
        var_scale,
        mode,
    ]


@np.vectorize
def fit_crisp_scale_center_pm_offsets(x, y, z, vx, vy, vz):
    """
    Triangular Fuzzy-Random value described like:
    - center = `y`
    - left = `y-x`
    - right = `y+z`

    Shift-Scale Representation based on Normal `shift` and crisp `scale`
    with Symmetric Triangular value Tr(0, 1)
    """
    shift = (3 * y - x + z) / 3
    scale = x + z

    var_shift = (3 * vy + vx + vz) / 3
    return [
        shift,
        scale,
        var_shift,
    ]


@np.vectorize
def fit_independent(x, y, z, vx, vy, vz):
    """
    Triangular Fuzzy-Random value described like:
    - center = `y`
    - left = `x`
    - right = `z`

    Shift-Scale Representation based on Normal `shift` and `scale`
    with Symmetric Triangular value Tr(`mode`, 1)
    """

    shift = (
        (1 / 12)
        * (
            -vx * x
            - 4 * vx * y
            - 7 * vx * z
            + 8 * vy * x
            + 8 * vy * y
            + 8 * vy * z
            - 7 * vz * x
            - 4 * vz * y
            - vz * z
        )
        / (-vx + 2 * vy - vz)
    )
    scale = -x + z
    var_shift = (
        (1 / 8)
        * (vx**2 - 8 * vx * vy - 2 * vx * vz + 16 * vy**2 - 8 * vy * vz + vz**2)
        / (-vx + 2 * vy - vz)
    )
    var_scale = 2 * vx - 4 * vy + 2 * vz
    mode = (vx - vz) / (-4 * vx + 8 * vy - 4 * vz)
    return [
        shift,
        scale,
        var_shift,
        var_scale,
        mode,
    ]
