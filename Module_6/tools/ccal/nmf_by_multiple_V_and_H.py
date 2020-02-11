from numpy import full, nan, sum
from numpy.random import random_sample, seed

from ._compute_norm import _compute_norm
from ._update_H_by_multiplicative_update import _update_H_by_multiplicative_update


def nmf_by_multiple_V_and_H(
    Vs, k, weights=None, n_iteration=int(1e3), random_seed=20121020
):

    R_norms = full((len(Vs), n_iteration + 1), nan)

    seed(random_seed)

    W = random_sample(size=(Vs[0].shape[0], k))

    Hs = [random_sample(size=(k, V.shape[1])) for V in Vs]

    R_norms[:, 0] = [_compute_norm(Vs[i] - W @ Hs[i]) for i in range(len(Vs))]

    V_0_norm = _compute_norm(Vs[0])

    if weights is None:

        weights = [V_0_norm / _compute_norm(V) for V in Vs]

    for j in range(n_iteration):

        top = sum([weights[i] * Vs[i] @ Hs[i].T for i in range(len(Vs))], axis=0)

        bottom = sum([weights[i] * W @ Hs[i] @ Hs[i].T for i in range(len(Vs))], axis=0)

        W *= top / bottom

        Hs = [
            _update_H_by_multiplicative_update(Vs[i], W, Hs[i]) for i in range(len(Vs))
        ]

        R_norms[:, j + 1] = [_compute_norm(Vs[i] - W @ Hs[i]) for i in range(len(Vs))]

        # TODO: stop based on tolerance

    return W, Hs, R_norms
