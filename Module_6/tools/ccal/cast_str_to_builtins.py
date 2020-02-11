def cast_str_to_builtins(str_):

    if str_ == "None":

        return None

    elif str_ == "True":

        return True

    elif str_ == "False":

        return False

    for type_ in (int, float):

        try:

            return type_(str_)

        except ValueError:

            pass

    return str_
