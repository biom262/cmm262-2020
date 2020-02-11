from subprocess import CalledProcessError

from .run_command import run_command


def have_program(program_name):

    try:

        return bool(run_command("which {}".format(program_name)).stdout.strip())

    except CalledProcessError:

        return False
