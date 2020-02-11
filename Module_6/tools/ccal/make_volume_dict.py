from .run_command import run_command


def make_volume_dict():

    volume_dict = {}

    for line in run_command("sudo blkid").stdout.strip("\n").split(sep="\n"):

        line = line.split()

        volume_name = line[0][:-1]

        volume_dict[volume_name] = {}

        for field_value in line[1:]:

            field, value = field_value.replace('"', "").split(sep="=")

            volume_dict[volume_name][field] = value

    return volume_dict
