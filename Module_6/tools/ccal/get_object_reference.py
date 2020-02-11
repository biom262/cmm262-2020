from .cast_str_to_builtins import cast_str_to_builtins


def get_object_reference(object_, namespace):

    for reference, object__ in namespace.items():

        if object__ is object_:

            return reference

    return cast_str_to_builtins(object_)
