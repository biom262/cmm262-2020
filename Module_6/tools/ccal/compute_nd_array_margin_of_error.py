from numpy import nan, sqrt
from scipy.stats import norm

from .check_nd_array_for_bad import check_nd_array_for_bad


def compute_nd_array_margin_of_error(nd_array, confidence=0.95, raise_for_bad=True):

    is_good = ~check_nd_array_for_bad(nd_array, raise_for_bad=raise_for_bad)

    if is_good.any():

        nd_array_good = nd_array[is_good]

        return norm.ppf(q=confidence) * nd_array_good.std() / sqrt(nd_array_good.size)

    else:

        return nan
