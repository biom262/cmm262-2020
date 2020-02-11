def get_unique_iterable_objects_in_order(iterable):

    unique_objects_in_order = []

    for object_ in iterable:

        if object_ not in unique_objects_in_order:

            unique_objects_in_order.append(object_)

    return unique_objects_in_order
