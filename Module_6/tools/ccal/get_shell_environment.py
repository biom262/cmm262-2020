from .run_command import run_command


def get_shell_environment():

    environemnt = {}

    for line in run_command("env").stdout.split(sep="\n"):

        if line and not line.strip().startswith(":"):

            key, value = line.split(sep="=", maxsplit=1)

            environemnt[key.strip()] = value.strip()

    return environemnt
