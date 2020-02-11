from numpy import full, nan
from numpy.random import get_state, seed, set_state, shuffle

from ._match_target_and_data import _match_target_and_data


def _permute_target_and_match_target_and_data(
    target,
    data,
    random_seed,
    n_permutation,
    match_function,
    n_required_for_match_function,
    raise_for_n_less_than_required,
):

    print("Computing p-value and FDR with {} permutation ...".format(n_permutation))

    seed(random_seed)

    index_x_permutation = full((data.shape[0], n_permutation), nan)

    permuted_target = target.copy()

    for i in range(n_permutation):

        shuffle(permuted_target)

        random_state = get_state()

        index_x_permutation[:, i] = _match_target_and_data(
            permuted_target,
            data,
            match_function,
            n_required_for_match_function,
            raise_for_n_less_than_required,
        )

        set_state(random_state)

    return index_x_permutation
