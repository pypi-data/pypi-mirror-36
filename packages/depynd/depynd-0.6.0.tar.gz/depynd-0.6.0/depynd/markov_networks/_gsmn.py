import numpy as np

from depynd.information import conditional_mutual_information


def _gsmn(X, lamb=0.0, **kwargs):
    """Learn the structure of Markov random field with glow-shrink Markov network [bromberg2009efficient]_.

    Parameters
    ----------
    X : array, shape (n_samples, n_features)
        Observations of variables.
    lamb: float
        Threshold for independence tests.
    kwargs : dict, default None
        Optional parameters for MI estimation.

    Returns
    ----------
    adj : array, shape (n_features, n_features)
        Estimated adjacency matrix of an MRF.

    References
    ----------
    .. [bromberg2009efficient] Bromberg, Facundo, Dimitris Margaritis, and Vasant Honavar. "Efficient Markov network
        structure discovery using independence tests." Journal of Artificial Intelligence Research 35 (2009): 449-484.
    """
    n, d = X.shape
    adj = np.zeros([d, d], dtype=bool)
    for i in range(d):
        adj_tmp = np.zeros([d, d], dtype=bool)
        adj_tmp = _grow(adj_tmp, i, X, lamb, **kwargs)
        adj_tmp = _shrink(adj_tmp, i, X, lamb, **kwargs)
        adj |= adj_tmp
    return adj


def _grow(adj, i, X, lamb, **kwargs):
    n, d = X.shape
    x = X[:, i]
    updated = True
    while updated:
        updated = False
        non_adj = ~adj[i] & (np.arange(d) != i)
        for j in non_adj.nonzero()[0]:
            y = X[:, j]
            z = X[:, adj[i]]
            cmi = conditional_mutual_information(x, y, z, **kwargs)
            if cmi > lamb:
                adj[i, j] = adj[j, i] = 1
                updated = True
                break
    return adj


def _shrink(adj, i, X, lamb, **kwargs):
    n, d = X.shape
    x = X[:, i]
    updated = True
    while updated:
        updated = False
        for j in adj[i].nonzero()[0]:
            other_adj = adj[i] & (np.arange(d) != j)
            y = X[:, j]
            z = X[:, other_adj]
            cmi = conditional_mutual_information(x, y, z, **kwargs)
            if cmi <= lamb:
                adj[i, j] = adj[j, i] = 0
                updated = True
                break
    return adj
