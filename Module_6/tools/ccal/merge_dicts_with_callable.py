def merge_dicts_with_callable(dict_0, dict_1, callable_):

    merged_dict = {}

    for key in dict_0.keys() | dict_1.keys():

        if key in dict_0 and key in dict_1:

            merged_dict[key] = callable_(dict_0[key], dict_1[key])

        elif key in dict_0:

            merged_dict[key] = dict_0[key]

        elif key in dict_1:

            merged_dict[key] = dict_1[key]

        else:

            raise ValueError("dict_0 or dict_1 changed during iteration.")

    return merged_dict
