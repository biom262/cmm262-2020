from subprocess import PIPE, run


def run_command(command, print_command=False):

    if print_command:

        print(command)

    return run(
        command,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        check=True,
        universal_newlines=True,
    )
