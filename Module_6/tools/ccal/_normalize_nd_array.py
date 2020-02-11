from numpy import full, nan
from scipy.stats import rankdata

from .check_nd_array_for_bad import check_nd_array_for_bad


def _normalize_nd_array(_nd_array, method, rank_method, raise_for_bad):

    is_good = ~check_nd_array_for_bad(_nd_array, raise_for_bad=raise_for_bad)

    nd_array_normalized = full(_nd_array.shape, nan)

    if is_good.any():

        nd_array_good = _nd_array[is_good]

        if method == "-0-":

            nd_array_good_std = nd_array_good.std()

            if nd_array_good_std == 0:

                nd_array_normalized[is_good] = 0

            else:

                nd_array_normalized[is_good] = (
                    nd_array_good - nd_array_good.mean()
                ) / nd_array_good_std

        elif method == "0-1":

            nd_array_good_min = nd_array_good.min()

            nd_array_good_range = nd_array_good.max() - nd_array_good_min

            if nd_array_good_range == 0:

                nd_array_normalized[is_good] = nan

            else:

                nd_array_normalized[is_good] = (
                    nd_array_good - nd_array_good_min
                ) / nd_array_good_range

        elif method == "sum":

            if nd_array_good.min() < 0:

                raise ValueError("Sum normalize only positives.")

            else:

                nd_array_good_sum = nd_array_good.sum()

                if nd_array_good_sum == 0:

                    nd_array_normalized[is_good] = 1 / is_good.sum()

                else:

                    nd_array_normalized[is_good] = nd_array_good / nd_array_good_sum

        elif method == "rank":

            nd_array_normalized[is_good] = rankdata(nd_array_good, method=rank_method)

    return nd_array_normalized
