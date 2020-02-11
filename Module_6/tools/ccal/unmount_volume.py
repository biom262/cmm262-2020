from .run_command import run_command


def unmount_volume(volume_name_or_mount_directory_path):

    run_command("sudo umount {}".format(volume_name_or_mount_directory_path))
