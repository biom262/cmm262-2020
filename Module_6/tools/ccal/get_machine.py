from platform import uname


def get_machine():

    uname_ = uname()

    return "{}_{}".format(uname_.system, uname_.machine)
