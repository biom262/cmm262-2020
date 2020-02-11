from numpy import full, nan

from .check_nd_array_for_bad import check_nd_array_for_bad


def clip_nd_array_by_standard_deviation(
    nd_array, n_standard_deviation, raise_for_bad=True
):

    is_good = ~check_nd_array_for_bad(nd_array, raise_for_bad=raise_for_bad)

    nd_array_clipped = full(nd_array.shape, nan)

    if is_good.any():

        nd_array_good = nd_array[is_good]

        nd_array_good_mean = nd_array_good.mean()

        nd_array_good_interval = nd_array_good.std() * n_standard_deviation

        nd_array_clipped[is_good] = nd_array[is_good].clip(
            min=nd_array_good_mean - nd_array_good_interval,
            max=nd_array_good_mean + nd_array_good_interval,
        )

    return nd_array_clipped
