from numpy import asarray, full, nan, where
from statsmodels.sandbox.stats.multicomp import multipletests

from .check_nd_array_for_bad import check_nd_array_for_bad
from .compute_empirical_p_value import compute_empirical_p_value


def compute_empirical_p_values_and_fdrs(
    values, random_values, p_value_direction, raise_for_bad=True
):

    is_good = ~check_nd_array_for_bad(values, raise_for_bad=raise_for_bad)

    is_good_random_value = ~check_nd_array_for_bad(
        random_values, raise_for_bad=raise_for_bad
    )

    p_values = full(values.shape, nan)

    fdrs = full(values.shape, nan)

    if is_good.any() and is_good_random_value.any():

        values_good = values[is_good]

        random_values_good = random_values[is_good_random_value]

        if "<" in p_value_direction:

            good_p_values_less = asarray(
                tuple(
                    compute_empirical_p_value(value_good, random_values_good, "<")
                    for value_good in values_good
                )
            )

            good_fdrs_less = multipletests(good_p_values_less, method="fdr_bh")[1]

        if ">" in p_value_direction:

            good_p_values_great = asarray(
                tuple(
                    compute_empirical_p_value(value_good, random_values_good, ">")
                    for value_good in values_good
                )
            )

            good_fdrs_great = multipletests(good_p_values_great, method="fdr_bh")[1]

        if p_value_direction == "<>":

            good_p_values = where(
                good_p_values_less < good_p_values_great,
                good_p_values_less,
                good_p_values_great,
            )

            good_fdrs = where(
                good_fdrs_less < good_fdrs_great, good_fdrs_less, good_fdrs_great
            )

        elif p_value_direction == "<":

            good_p_values = good_p_values_less

            good_fdrs = good_fdrs_less

        elif p_value_direction == ">":

            good_p_values = good_p_values_great

            good_fdrs = good_fdrs_great

        p_values[is_good] = good_p_values

        fdrs[is_good] = good_fdrs

    return p_values, fdrs
