from .make_volume_dict import make_volume_dict


def get_volume_name(volume_label):

    volume_dict = make_volume_dict()

    for volume_name, dict_ in volume_dict.items():

        if dict_.get("LABEL") == volume_label:

            return volume_name
