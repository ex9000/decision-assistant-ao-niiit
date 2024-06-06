from math import pi, acos, cos, sin

import numpy as np


def adjust_corr_matrix(corr, i, j, val):
    """Adjusting correlation matrix, to achieve desired correlation value between i-th & j-th item"""
    assert corr.ndim == 2

    h, w = corr.shape
    assert h == w
    assert 0 <= i < h
    assert 0 <= j < h
    assert i != j

    # find target vectors on a plain
    alpha = 0.5 * (pi - acos(val))
    p = np.array([cos(alpha), sin(alpha)])
    q = np.array([cos(pi - alpha), sin(pi - alpha)])

    # decompose correlation matrix to vectors
    ch_vecs = np.linalg.cholesky(corr).T

    # extract i-th and j-tj vectors
    a, b = ch_vecs[:, i], ch_vecs[:, j]

    # build orthogonal plain basis
    u, v = a - b, a + b
    u /= np.linalg.norm(u)
    v /= np.linalg.norm(v)
    basis = np.stack([u, v], axis=1)

    # get new vectors using basis
    a2 = basis @ p
    b2 = basis @ q

    # update set of vectors
    ch_vecs[:, i], ch_vecs[:, j] = a2, b2

    # get fixed correlation matrix from vectors
    corr_fixed = ch_vecs.T @ ch_vecs

    return corr_fixed
