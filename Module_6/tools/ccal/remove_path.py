from os import remove
from os.path import exists, isdir
from shutil import rmtree
from warnings import warn


def remove_path(path, print_=True):

    if isdir(path):

        rmtree(path)

        removed_path = True

    elif exists(path):

        remove(path)

        removed_path = True

    else:

        warn("Could not remove {} because it does not exist.".format(path))

        removed_path = False

    if removed_path and print_:

        print("Removed {}.".format(path))
