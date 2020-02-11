from .run_command import run_command


def get_conda_environments():

    environments = {}

    for line in run_command("conda-env list").stdout.strip().split(sep="\n"):

        if not line.startswith("#"):

            environment, path = (split for split in line.split() if split != "*")

            environments[environment] = {"path": path}

    return environments
