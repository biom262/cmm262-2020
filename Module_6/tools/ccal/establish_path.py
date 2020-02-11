from os import mkdir
from os.path import isdir, split

from .clean_path import clean_path


def establish_path(path, path_type, print_=True):

    path = clean_path(path)

    if path_type == "file":

        if path.endswith("/"):

            raise ValueError("File path {} should not end with '/'.".format(path))

    elif path_type == "directory":

        if not path.endswith("/"):

            path += "/"

    else:

        raise ValueError("Unknown path_type: {}.".format(path_type))

    directory_path, file_name = split(path)

    missing_directory_paths = []

    while not isdir(directory_path):

        missing_directory_paths.append(directory_path)

        directory_path, file_name = split(directory_path)

    for directory_path in reversed(missing_directory_paths):

        mkdir(directory_path)

        if print_:

            print("Created directory {}.".format(directory_path))
