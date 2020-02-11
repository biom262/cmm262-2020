from .get_unique_iterable_objects_in_order import get_unique_iterable_objects_in_order


def make_object_int_mapping(iterable):

    object_int = {}

    int_object = {}

    for int_, object in enumerate(get_unique_iterable_objects_in_order(iterable)):

        object_int[object] = int_

        int_object[int_] = object

    return object_int, int_object
