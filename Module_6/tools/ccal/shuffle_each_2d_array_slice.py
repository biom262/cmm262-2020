from numpy.random import seed, shuffle

from .check_nd_array_for_bad import check_nd_array_for_bad


def shuffle_each_2d_array_slice(
    _2d_array, axis, random_seed=20121020, raise_for_bad=True
):

    check_nd_array_for_bad(_2d_array, raise_for_bad=raise_for_bad)

    _2d_array = _2d_array.copy()

    seed(random_seed)

    if axis == 0:

        for i in range(_2d_array.shape[1]):

            shuffle(_2d_array[:, i])

    elif axis == 1:

        for i in range(_2d_array.shape[0]):

            shuffle(_2d_array[i, :])

    return _2d_array
