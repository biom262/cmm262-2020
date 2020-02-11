from .apply_function_on_2_1d_arrays import apply_function_on_2_1d_arrays


def _ignore_bad_and_compute_euclidean_distance_between_2_1d_arrays(
    _1d_array_0, _1d_array_1
):

    return apply_function_on_2_1d_arrays(
        _1d_array_0,
        _1d_array_1,
        lambda _1d_array_0, _1d_array_1: ((_1d_array_0 - _1d_array_1) ** 2).sum()
        ** (1 / 2),
        raise_for_bad=False,
    )
