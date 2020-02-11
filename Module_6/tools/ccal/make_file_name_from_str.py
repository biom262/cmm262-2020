from re import sub


def make_file_name_from_str(str_):

    return sub(r"(?u)[^-\w.]", "", str_.strip().replace(" ", "_"))
