from sys import exit

from .echo_or_print import echo_or_print


def exit_(str_, exception=None):

    echo_or_print("Uh oh :( ... {}".format(str_), fg="red", bg="black")

    if exception is None:

        exit()

    else:

        raise exception
