from .run_command import run_command


def shutdown_machine():

    run_command("sudo shutdown -h now")
