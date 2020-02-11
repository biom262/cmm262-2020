from subprocess import PIPE, CalledProcessError, Popen

from .exit_ import exit_


def run_command_and_monitor(command, print_command=False):

    if print_command:

        print(command)

    process = Popen(
        command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True
    )

    for line in process.stdout:

        print(line.strip())

    if process.poll():

        exit_(
            "\n".join(process.stderr),
            exception=CalledProcessError(
                process.returncode, command, stderr=process.stderr
            ),
        )
