from os import listdir
from os.path import isdir, isfile, islink

from .remove_path import remove_path


def remove_paths(directory_path, path_type, print_=True):

    for name in listdir(directory_path):

        path = "{}/{}".format(directory_path, name)

        if path_type not in ("file", "directory", "link"):

            raise ValueError("Unknown path_type: {}.".format(path_type))

        if (
            (path_type == "file" and isfile(path))
            or (path_type == "directory" and isdir(path))
            or (path_type == "link" and islink(path))
        ):

            remove_path(path, print_=print_)
