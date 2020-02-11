from warnings import warn

from pandas import Series

from .cast_str_to_builtins import cast_str_to_builtins
from .replace_bad_objects_in_iterable import replace_bad_objects_in_iterable


def cast_series_to_builtins(series):

    list_ = replace_bad_objects_in_iterable(
        tuple(cast_str_to_builtins(object_) for object_ in series)
    )

    try:

        return Series(list_, index=series.index, dtype=float)

    except (TypeError, ValueError) as exception:

        warn(exception)

        return Series(list_, index=series.index)
