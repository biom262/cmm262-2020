from .run_command import run_command


def _print_and_run_command(command):

    print()

    return run_command(command, print_command=True)
