from json import dump


def write_json(json_dict, json_file_path, indent=2):

    with open(json_file_path, "w") as json_file:

        dump(json_dict, json_file, indent=indent)
