from numpy import apply_along_axis

from ._normalize_nd_array import _normalize_nd_array


def normalize_nd_array(
    nd_array, axis, method, rank_method="average", raise_for_bad=True
):

    if axis is None:

        return _normalize_nd_array(nd_array, method, rank_method, raise_for_bad)

    else:

        return apply_along_axis(
            _normalize_nd_array, axis, nd_array, method, rank_method, raise_for_bad
        )
