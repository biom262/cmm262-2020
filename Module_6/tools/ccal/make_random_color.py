from numpy.random import choice


def make_random_color(format_):

    if format_ == "hex":

        return "#{}{}{}{}{}{}".format(*choice(list("0123456789abcdef"), size=6))
