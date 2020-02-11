from numpy import diff, insert, sign

from .check_nd_array_for_bad import check_nd_array_for_bad


def get_intersections_between_2_1d_arrays(_1d_array_0, _1d_array_1, raise_for_bad=True):

    check_nd_array_for_bad(_1d_array_0, raise_for_bad=raise_for_bad)

    check_nd_array_for_bad(_1d_array_1, raise_for_bad=raise_for_bad)

    diff_sign = sign(_1d_array_0 - _1d_array_1)

    diff_sign_0_indices = (diff_sign == 0).nonzero()[0]

    if diff_sign_0_indices.size:

        diff_sign[diff_sign_0_indices] = diff_sign[diff_sign_0_indices + 1]

    return insert(diff(diff_sign) != 0, 0, False)
