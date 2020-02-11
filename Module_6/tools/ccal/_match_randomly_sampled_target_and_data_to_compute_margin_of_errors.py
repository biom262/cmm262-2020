from math import ceil

from numpy import apply_along_axis, full, nan
from numpy.random import choice, get_state, seed, set_state

from ._match_target_and_data import _match_target_and_data
from .compute_nd_array_margin_of_error import compute_nd_array_margin_of_error


def _match_randomly_sampled_target_and_data_to_compute_margin_of_errors(
    target,
    data,
    random_seed,
    n_sampling,
    match_function,
    n_required_for_match_function,
    raise_for_n_less_than_required,
):

    print("Computing MoE with {} sampling ...".format(n_sampling))

    seed(random_seed)

    index_x_sampling = full((data.shape[0], n_sampling), nan)

    n_sample = ceil(0.632 * target.size)

    for i in range(n_sampling):

        random_indices = choice(target.size, size=n_sample, replace=True)

        sampled_target = target[random_indices]

        sampled_data = data[:, random_indices]

        random_state = get_state()

        index_x_sampling[:, i] = _match_target_and_data(
            sampled_target,
            sampled_data,
            match_function,
            n_required_for_match_function,
            raise_for_n_less_than_required,
        )

        set_state(random_state)

    return apply_along_axis(
        compute_nd_array_margin_of_error, 1, index_x_sampling, raise_for_bad=False
    )
