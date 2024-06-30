from src.fuzzy import TriangleSymmetric
from src.probability import Normal
from .bare_numbers import (
    fit_independent,
    fit_center_pm_offsets,
    fit_crisp_scale_center_pm_offsets,
)


def fit_cslsr(
    center: Normal, shift_left: Normal, shift_right: Normal
) -> TriangleSymmetric[Normal]:
    """Center, shift left, shift right"""

    shift, scale, var_shift, var_scale, mode = fit_center_pm_offsets(
        shift_left.mu,
        center.mu,
        shift_right.mu,
        shift_left.sigma2,
        center.sigma2,
        shift_right.sigma2,
    )

    shift = Normal(shift, var_shift)
    scale = Normal(scale, var_scale)
    fuzzy = TriangleSymmetric(mode, 1)

    return shift + scale * fuzzy


def fit_crisp_cslsr(
    center: Normal, shift_left: Normal, shift_right: Normal
) -> TriangleSymmetric[Normal]:
    """Center, shift left, shift right"""

    shift, scale, var_shift = fit_crisp_scale_center_pm_offsets(
        shift_left.mu,
        center.mu,
        shift_right.mu,
        shift_left.sigma2,
        center.sigma2,
        shift_right.sigma2,
    )

    shift = Normal(shift, var_shift)
    fuzzy = TriangleSymmetric(0, 1)

    return shift + scale * fuzzy


def fit_lcr(left: Normal, center: Normal, right: Normal) -> TriangleSymmetric[Normal]:
    """Left, center,  right"""

    shift, scale, var_shift, var_scale, mode = fit_independent(
        left.mu,
        center.mu,
        right.mu,
        left.sigma2,
        center.sigma2,
        right.sigma2,
    )

    shift = Normal(shift, var_shift)
    scale = Normal(scale, var_scale)
    fuzzy = TriangleSymmetric(mode, 1)

    return shift + scale * fuzzy
