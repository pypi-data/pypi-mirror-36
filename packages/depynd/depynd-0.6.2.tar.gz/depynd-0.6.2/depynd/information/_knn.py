import numpy as np
from scipy.special import digamma


def _mi_knn(X, Y, n_neighbors):
    """Estimate mutual information between X and Y using kNN-based MI estimator.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features_x) or (n_samples)
        Observations of a variable.
    Y : array-like, shape (n_samples, n_features_y) or (n_samples)
        Observations of the other variable.
    n_neighbors : int
        Number of neighbors.

    Returns
    -------
    mi : float
        Estimated mutual information between ``X`` and ``Y``.
    """
    n, d_x = X.shape
    _, d_y = Y.shape
    distances_x = np.linalg.norm(X - X.reshape([n, -1, d_x]), axis=2)
    distances_y = np.linalg.norm(Y - Y.reshape([n, -1, d_y]), axis=2)
    distances = np.maximum(distances_x, distances_y)
    epsilons = np.partition(distances, n_neighbors, axis=1)[:, n_neighbors]
    idx_discrete = np.isclose(epsilons, 0)
    ks = np.repeat(n_neighbors, n)
    ks[idx_discrete] = np.sum(np.isclose(distances[idx_discrete], 0), axis=1) - 1
    n_x = np.sum(distances_x <= epsilons, axis=0) - 1
    n_y = np.sum(distances_y <= epsilons, axis=0) - 1
    mi = np.log(n) + np.mean(digamma(ks) - np.log(n_x * n_y))
    return mi
