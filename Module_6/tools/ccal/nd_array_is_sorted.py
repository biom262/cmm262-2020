from numpy import diff

from .check_nd_array_for_bad import check_nd_array_for_bad


def nd_array_is_sorted(nd_array, raise_for_bad=True):

    check_nd_array_for_bad(nd_array, raise_for_bad=raise_for_bad)

    diff_ = diff(nd_array)

    return (diff_ <= 0).all() or (0 <= diff_).all()
