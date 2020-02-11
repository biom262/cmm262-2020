from warnings import warn

from numpy import isinf, isnan


def check_nd_array_for_bad(nd_array, raise_for_bad=True):

    bads = []

    is_nan = isnan(nd_array)

    if is_nan.any():

        bads.append("nan")

    is_inf = isinf(nd_array)

    if is_inf.any():

        bads.append("inf")

    is_bad = is_nan | is_inf

    n_bad = is_bad.sum()

    if 0 < n_bad:

        message = "{} good & {} bad ({}).".format(
            nd_array.size - n_bad, n_bad, ", ".join(bads)
        )

        if raise_for_bad:

            raise ValueError(message)

        else:

            warn(message)

    return is_bad
