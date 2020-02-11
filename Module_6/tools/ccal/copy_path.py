from os.path import exists, isdir
from shutil import copy, copytree
from warnings import warn

from .remove_path import remove_path


def copy_path(from_path, to_path, overwrite=False, print_=True):

    if overwrite:

        remove_path(to_path, print_=print_)

    if isdir(from_path):

        copytree(from_path, to_path)

        copied_path = True

    elif exists(from_path):

        copy(from_path, to_path)

        copied_path = True

    else:

        warn("Could not copy {} because it does not exist.".format(from_path))

        copied_path = False

    if copied_path and print_:

        print("Copied {} =(to)=> {}.".format(from_path, to_path))
