from os.path import isdir

from .run_command import run_command


def mount_volume(volume_name, mount_directory_path):

    if not isdir(mount_directory_path):

        raise ValueError(
            "{0} does not exist. Make it by\n$ sudo mkdir -pv {0}".format(
                mount_directory_path
            )
        )

    run_command("sudo mount {} {}".format(volume_name, mount_directory_path))
