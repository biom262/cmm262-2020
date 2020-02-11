from os.path import abspath, expanduser


def clean_path(path):

    return abspath(expanduser(path))
