from numpy import asarray

from .check_nd_array_for_bad import check_nd_array_for_bad


def get_1d_array_unique_objects_in_order(_1d_array, raise_for_bad=True):

    check_nd_array_for_bad(_1d_array, raise_for_bad=raise_for_bad)

    unique_objects_in_order = []

    for object_ in _1d_array:

        if object_ not in unique_objects_in_order:

            unique_objects_in_order.append(object_)

    return asarray(unique_objects_in_order)
