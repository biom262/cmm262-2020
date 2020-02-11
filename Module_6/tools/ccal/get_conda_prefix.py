from os import environ


def get_conda_prefix():

    return environ.get("CONDA_PREFIX")
