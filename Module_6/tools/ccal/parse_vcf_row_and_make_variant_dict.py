from .VCF_ANN_FIELDS import VCF_ANN_FIELDS
from .VCF_COLUMNS import VCF_COLUMNS


def parse_vcf_row_and_make_variant_dict(vcf_row, n_info_ann=None):

    variant_dict = {
        column: vcf_row[i]
        for i, column in enumerate(VCF_COLUMNS[: VCF_COLUMNS.index("FILTER") + 1])
    }

    info_without_field = []

    for info in vcf_row[VCF_COLUMNS.index("INFO")].split(sep=";"):

        if "=" in info:

            info_field, info_value = info.split(sep="=")

            if info_field == "ANN":

                variant_dict["ANN"] = {}

                for ann_index, ann in enumerate(info_value.split(sep=",")[:n_info_ann]):

                    ann_values = ann.split(sep="|")

                    variant_dict["ANN"][ann_index] = {
                        ann_field: ann_values[ann_field_index + 1]
                        for ann_field_index, ann_field in enumerate(VCF_ANN_FIELDS[1:])
                    }

            else:

                variant_dict[info_field] = info_value

        else:

            info_without_field.append(info)

    if len(info_without_field):

        variant_dict["INFO_without_field"] = ";".join(info_without_field)

    vcf_column_format_index = VCF_COLUMNS.index("FORMAT")

    format_fields = vcf_row[vcf_column_format_index].split(sep=":")

    variant_dict["sample"] = {}

    for sample_index, sample in enumerate(vcf_row[vcf_column_format_index + 1 :]):

        variant_dict["sample"][sample_index] = {
            format_field: sample_value
            for format_field, sample_value in zip(format_fields, sample.split(sep=":"))
        }

    return variant_dict
