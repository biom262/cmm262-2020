from .run_command import run_command


def get_installed_pip_libraries():

    return [
        line.split()[0]
        for line in run_command("pip list").stdout.strip().split(sep="\n")[2:]
    ]
