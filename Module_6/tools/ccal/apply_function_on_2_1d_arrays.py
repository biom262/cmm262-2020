from warnings import warn

from numpy import full, nan
from numpy.random import seed, shuffle

from .check_nd_array_for_bad import check_nd_array_for_bad
from .compute_empirical_p_value import compute_empirical_p_value


def apply_function_on_2_1d_arrays(
    _1d_array_0,
    _1d_array_1,
    function,
    n_required=None,
    raise_for_n_less_than_required=True,
    n_permutation=0,
    random_seed=20121020,
    p_value_direction=None,
    raise_for_bad=True,
    use_only_good=True,
):

    is_good_0 = ~check_nd_array_for_bad(_1d_array_0, raise_for_bad=raise_for_bad)

    is_good_1 = ~check_nd_array_for_bad(_1d_array_1, raise_for_bad=raise_for_bad)

    if use_only_good:

        is_good = is_good_0 & is_good_1

        if n_required is not None:

            if n_required <= 1:

                n_required *= is_good.size

            if is_good.sum() < n_required:

                message = "{} requires {} <= n.".format(function.__name__, n_required)

                if raise_for_n_less_than_required:

                    raise ValueError(message)

                else:

                    warn(message)

                    return nan

        _1d_array_good_0 = _1d_array_0[is_good]

        _1d_array_good_1 = _1d_array_1[is_good]

    else:

        _1d_array_good_0 = _1d_array_0[is_good_0]

        _1d_array_good_1 = _1d_array_1[is_good_1]

    value = function(_1d_array_good_0, _1d_array_good_1)

    if 0 < n_permutation:

        random_values = full(n_permutation, nan)

        _1d_array_good_0_shuffled = _1d_array_good_0.copy()

        seed(random_seed)

        for i in range(n_permutation):

            shuffle(_1d_array_good_0_shuffled)

            random_values[i] = function(_1d_array_good_0_shuffled, _1d_array_good_1)

        return (
            value,
            compute_empirical_p_value(
                value, random_values, p_value_direction, raise_for_bad=raise_for_bad
            ),
        )

    else:

        return value
