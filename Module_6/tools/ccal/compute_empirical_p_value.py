from numpy import isnan, nan

from .check_nd_array_for_bad import check_nd_array_for_bad


def compute_empirical_p_value(
    value, random_values, p_value_direction, raise_for_bad=True
):

    if isnan(value):

        return nan

    is_good = ~check_nd_array_for_bad(random_values, raise_for_bad=raise_for_bad)

    if is_good.any():

        random_values_good = random_values[is_good]

        if p_value_direction == "<":

            n_significant_random_value = (random_values_good <= value).sum()

        elif p_value_direction == ">":

            n_significant_random_value = (value <= random_values_good).sum()

        return max(1, n_significant_random_value) / random_values_good.size

    else:

        return nan
