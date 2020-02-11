from numpy import asarray, mean

from .get_unique_iterable_objects_in_order import get_unique_iterable_objects_in_order


def group_and_apply_function_on_each_group_in_iterable(
    iterable, groups, callable_=mean
):

    unique_groups_in_order = get_unique_iterable_objects_in_order(groups)

    applied_by_group = []

    for group in unique_groups_in_order:

        applied_by_group.append(callable_(asarray(iterable)[groups == group]))

    return unique_groups_in_order, applied_by_group
