from gzip import open as gzip_open

from pandas import read_csv

from ._describe_vcf_df import _describe_vcf_df
from ._make_clean_vcf_df import _make_clean_vcf_df
from .parse_vcf_row_and_make_variant_dict import parse_vcf_row_and_make_variant_dict
from .split_str_ignoring_inside_quotes import split_str_ignoring_inside_quotes


def read_vcf_gz_and_make_vcf_dict(vcf_gz_file_path, simplify=True, n_info_ann=1):

    vcf_dict = {
        "meta_information": {},
        "vcf_df": None,
        "variant_dict": [],
        "clean_vcf_df": None,
    }

    print("\nParsing meta-information lines ...")

    with gzip_open(vcf_gz_file_path) as vcf_gz_file:

        n_row_to_skip = 0

        for line in vcf_gz_file:

            line = line.decode()

            if line.startswith("##"):

                n_row_to_skip += 1

                line = line[2:]

                field, value = line.split("=", maxsplit=1)

                if not (value.startswith("<") and value.endswith(">")):

                    vcf_dict["meta_information"][field] = value

                else:

                    value = value.strip("<>")

                    value_split = split_str_ignoring_inside_quotes(value, ",")

                    id_, id_name = value_split.pop(0).split(sep="=")

                    if id_ != "ID":

                        raise ValueError("ID must be the 1st value in {}.".format(line))

                    id_dict = {
                        field: value.strip("'\"")
                        for field, value in (
                            field_value.split("=", maxsplit=1)
                            for field_value in value_split
                        )
                    }

                    if field in vcf_dict["meta_information"]:

                        if id_name in vcf_dict["meta_information"][field]:

                            raise ValueError("Duplicated ID {}.".format(id_name))

                        else:

                            vcf_dict["meta_information"][field][id_name] = id_dict

                    else:

                        vcf_dict["meta_information"][field] = {id_name: id_dict}

            else:

                break

    print("\nReading .vcf DataFrame ...")

    vcf_df = read_csv(vcf_gz_file_path, sep="\t", skiprows=n_row_to_skip)

    columns = vcf_df.columns.tolist()

    columns[0] = columns[0][1:]

    vcf_df.columns = columns

    vcf_dict["vcf_df"] = vcf_df

    _describe_vcf_df(vcf_dict["vcf_df"])

    if simplify:

        print("\nMaking variant dicts ...")

        vcf_dict["variant_dict"] = vcf_df.apply(
            parse_vcf_row_and_make_variant_dict, axis=1, n_info_ann=n_info_ann
        ).tolist()

        print("\nMaking clean .vcf DataFrame ...")

        vcf_dict["clean_vcf_df"] = _make_clean_vcf_df(vcf_dict["variant_dict"])

    return vcf_dict
