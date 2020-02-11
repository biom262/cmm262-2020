def group_iterable(iterable, n, keep_leftover_group=False):

    groups = []

    group = []

    for object_ in iterable:

        group.append(object_)

        if len(group) == n:

            groups.append(group)

            group = []

    if len(group) != 0 and (len(group) == n or keep_leftover_group):

        groups.append(group)

    return groups
