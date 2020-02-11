from os.path import isdir


def conda_is_installed(conda_directory_path):

    return all(
        (isdir("{}/{}".format(conda_directory_path, name)) for name in ("bin", "lib"))
    )
