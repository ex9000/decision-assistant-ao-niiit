from bare_numbers import fit_independent, fit_center_pm_offsets
from src.fuzzy import TriangleSymmetric
from src.probability import Normal


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
