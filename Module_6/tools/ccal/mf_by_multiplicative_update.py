from numpy import full, nan
from numpy.random import random_sample, seed

from ._compute_norm import _compute_norm
from ._update_H_by_multiplicative_update import _update_H_by_multiplicative_update
from ._update_W_by_multiplicative_update import _update_W_by_multiplicative_update


def mf_by_multiplicative_update(V, k, n_iteration=int(1e3), random_seed=20121020):

    R_norms = full(n_iteration + 1, nan)

    seed(random_seed)

    W = random_sample(size=(V.shape[0], k))

    H = random_sample(size=(k, V.shape[1]))

    R_norms[0] = _compute_norm(V - W @ H)

    for i in range(n_iteration):

        W = _update_W_by_multiplicative_update(V, W, H)

        H = _update_H_by_multiplicative_update(V, W, H)

        R_norms[i + 1] = _compute_norm(V - W @ H)

        # TODO: stop based on tolerance

    return W, H, R_norms
