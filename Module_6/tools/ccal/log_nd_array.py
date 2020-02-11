from numpy import full
from numpy import log as loge
from numpy import log2, log10, nan

from .check_nd_array_for_bad import check_nd_array_for_bad


def log_nd_array(
    nd_array,
    shift_as_necessary_to_achieve_min_before_logging=None,
    log_base="e",
    raise_for_bad=True,
):

    is_good = ~check_nd_array_for_bad(nd_array, raise_for_bad=raise_for_bad)

    nd_array_logged = full(nd_array.shape, nan)

    if is_good.any():

        nd_array_good = nd_array[is_good]

        if shift_as_necessary_to_achieve_min_before_logging is not None:

            min_ = nd_array_good.min()

            if shift_as_necessary_to_achieve_min_before_logging == "0<":

                shift_as_necessary_to_achieve_min_before_logging = nd_array_good[
                    0 < nd_array_good
                ].min()

            if min_ < shift_as_necessary_to_achieve_min_before_logging:

                nd_array_good = (
                    nd_array_good
                    + shift_as_necessary_to_achieve_min_before_logging
                    - min_
                )

        if log_base in (2, "2"):

            log = log2

        elif log_base == "e":

            log = loge

        elif log_base in (10, "10"):

            log = log10

        nd_array_logged[is_good] = log(nd_array_good)

    return nd_array_logged
