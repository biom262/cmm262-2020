from os import environ


def add_conda_to_path(conda_directory_path):

    environ["PATH"] = "{}:{}".format(
        "{}/{}".format(conda_directory_path, "bin"), environ["PATH"]
    )
