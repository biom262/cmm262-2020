def flatten_nested_iterable(iterable, iterable_types=(list, tuple)):

    list_ = list(iterable)

    i = 0

    while i < len(list_):

        while isinstance(list_[i], iterable_types):

            if not len(list_[i]):

                list_.pop(i)

                i -= 1

                break

            else:

                list_[i : i + 1] = list_[i]

        i += 1

    return list_
