from subprocess import CalledProcessError

from .echo_or_print import echo_or_print
from .run_command import run_command


def in_git_repository():

    echo_or_print("Checking if in git repository ...")

    try:

        run_command("git status")

        return True

    except CalledProcessError:

        return False
