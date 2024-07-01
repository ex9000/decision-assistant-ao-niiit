import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


def best_figsize(matrix_size):
    return 2 + 0.3 * matrix_size, 2 + 0.3 * matrix_size


def cluster_corr(corr_array, inplace=False):
    """
    link: https://web.archive.org/web/20231001075317/https://wil.yegelwel.com/cluster-correlation-matrix/

    Rearranges the correlation matrix, corr_array, so that groups of highly
    correlated variables are next to each other

    Parameters
    ----------
    corr_array : pandas.DataFrame or numpy.ndarray
        a NxN correlation matrix
    inplace : bool, optional
        changing rows/columns order inplace

    Returns
    -------
    pandas.DataFrame or numpy.ndarray
        a NxN correlation matrix with the columns and rows rearranged
    """
    # mx = copy(corr_array).to_numpy()
    # mx *= 1 - np.eye(mx.shape[1])
    pairwise_distances = sch.distance.pdist(corr_array)
    linkage = sch.linkage(pairwise_distances, method="complete")
    cluster_distance_threshold = 0.5 * pairwise_distances.max()
    idx_to_cluster_array = sch.fcluster(
        linkage, cluster_distance_threshold, criterion="distance"
    )
    idx = np.argsort(idx_to_cluster_array)

    if not inplace:
        corr_array = corr_array.copy()

    if isinstance(corr_array, pd.DataFrame):
        return corr_array.iloc[idx, :].T.iloc[idx, :]
    return corr_array[idx, :][:, idx]


def plot_matrix(
    ax: Axes,
    matrix: pd.DataFrame,
    values_format: str = None,
    fontsize="medium",
    clustering=True,
    scale=1,
):
    w, h = matrix.shape
    if clustering and w == h:  # only if matrix is square
        matrix = cluster_corr(matrix)

    drawn = ax.matshow(
        matrix,
        cmap="bwr",
        vmin=-scale,
        vmax=scale,
        interpolation="none",
    )

    x_labels, y_labels = [range(size) for size in matrix.shape]
    ax.set_xticks(x_labels)
    ax.set_yticks(y_labels)

    if isinstance(matrix, pd.DataFrame):
        x_labels = matrix.columns
        y_labels = matrix.index
    ax.set_yticklabels(y_labels)
    ax.set_xticklabels(x_labels, rotation=-45, ha="right")

    # magic_kwargs make colorbar be the same size as matrix
    magic_kwargs = dict(fraction=0.046, pad=0.04)
    plt.colorbar(drawn, ax=ax, **magic_kwargs)

    if values_format is not None:
        # Loop over data dimensions and create text annotations.
        h, w = matrix.shape
        for i in range(h):
            for j in range(w):
                ax.text(
                    j,
                    i,
                    values_format.format(matrix.iloc[i, j]),
                    ha="center",
                    va="center",
                    color="w" if abs(matrix.iloc[i, j]) > 0.55 * scale else "black",
                    fontsize=fontsize,
                )
