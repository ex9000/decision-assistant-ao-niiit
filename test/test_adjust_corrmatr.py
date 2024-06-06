import numpy as np
import pytest

from src.algebra import adjust_corr_matrix


@pytest.mark.parametrize("seed", [42, 101, 202, 303, 404, 505])
def test_adjust_corr_matrix(seed):
    size = 13
    i, j, v = seed % size, 2 * seed % size, (seed % 2) - 0.5 * 1.9

    np.random.seed(seed)

    vectors = np.random.random((size, size)) - 0.5
    vectors /= np.sqrt((vectors ** 2).sum(axis=0))

    assert np.allclose((vectors ** 2).sum(axis=0), 1)

    corr = vectors.T @ vectors

    ls = np.linalg.eigvalsh(corr)
    assert np.all(ls >= 0)

    corr_fixed = adjust_corr_matrix(corr, i, j, v)
    assert corr_fixed[i, j] == pytest.approx(v)
    assert corr_fixed[j, i] == pytest.approx(v)

    ls = np.linalg.eigvalsh(corr_fixed)
    assert np.all(ls >= 0)
