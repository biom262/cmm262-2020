from pandas import Series


def write_dict(dict_, key_name, value_name, file_path):

    series = Series(dict_, name=value_name)

    series.index.name = key_name

    if not file_path.endswith(".tsv"):

        file_path += ".tsv"

    series.to_csv(file_path, sep="\t")
