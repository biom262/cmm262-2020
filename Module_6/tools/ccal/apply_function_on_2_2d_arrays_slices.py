from numpy import full, nan

from .apply_function_on_2_1d_arrays import apply_function_on_2_1d_arrays
from .check_nd_array_for_bad import check_nd_array_for_bad


def apply_function_on_2_2d_arrays_slices(
    _2d_array_0,
    _2d_array_1,
    function,
    axis,
    n_required=None,
    raise_for_n_less_than_required=True,
    raise_for_bad=True,
    use_only_good=True,
):

    check_nd_array_for_bad(_2d_array_0, raise_for_bad=raise_for_bad)

    check_nd_array_for_bad(_2d_array_1, raise_for_bad=raise_for_bad)

    if axis == 0:

        _2d_array_0 = _2d_array_0.T

        _2d_array_1 = _2d_array_1.T

    _2d_array = full((_2d_array_0.shape[0], _2d_array_1.shape[0]), nan)

    for i_0 in range(_2d_array_0.shape[0]):

        _2d_array_0_slice = _2d_array_0[i_0]

        for i_1 in range(_2d_array_1.shape[0]):

            _2d_array[i_0, i_1] = apply_function_on_2_1d_arrays(
                _2d_array_0_slice,
                _2d_array_1[i_1],
                function,
                n_required=n_required,
                raise_for_n_less_than_required=raise_for_n_less_than_required,
                raise_for_bad=raise_for_bad,
                use_only_good=use_only_good,
            )

    return _2d_array
