from numpy import where


def replace_bad_objects_in_iterable(
    iterable,
    bad_objects=("--", "unknown", "n/a", "N/A", "na", "NA", "nan", "NaN", "NAN"),
    replacement=None,
):

    return tuple(
        where(object_ in bad_objects, replacement, object_) for object_ in iterable
    )
