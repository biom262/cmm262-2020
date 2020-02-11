from inspect import stack


def get_function_name():

    return stack()[1][3]
