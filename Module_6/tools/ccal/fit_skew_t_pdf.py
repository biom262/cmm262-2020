from warnings import warn

from statsmodels.sandbox.distributions.extras import ACSkewT_gen

from .ALMOST_ZERO import ALMOST_ZERO
from .check_nd_array_for_bad import check_nd_array_for_bad


def fit_skew_t_pdf(_1d_array, fit_initial_location=None, fit_initial_scale=None):

    _1d_array = _1d_array[~check_nd_array_for_bad(_1d_array, raise_for_bad=False)]

    keyword_arguments = {}

    mean = _1d_array.mean()

    if abs(mean) <= ALMOST_ZERO:

        mean = 0

    keyword_arguments["loc"] = mean

    keyword_arguments["scale"] = _1d_array.std() / 2

    skew_t_model = ACSkewT_gen()

    degree_of_freedom, shape, location, scale = skew_t_model.fit(
        _1d_array, **keyword_arguments
    )

    if 24 < abs(shape):

        warn("Refitting with fixed scale ...")

        keyword_arguments["fscale"] = keyword_arguments["scale"]

        degree_of_freedom, shape, location, scale = skew_t_model.fit(
            _1d_array, **keyword_arguments
        )

        if 24 < abs(shape):

            warn("Refitting with fixed location ...")

            keyword_arguments["floc"] = keyword_arguments["loc"]

            degree_of_freedom, shape, location, scale = skew_t_model.fit(
                _1d_array, **keyword_arguments
            )

    return _1d_array.size, location, scale, degree_of_freedom, shape
