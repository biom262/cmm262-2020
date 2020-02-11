from pandas import DataFrame

from .VCF_COLUMNS import VCF_COLUMNS


def _make_clean_vcf_df(variant_dicts):

    vcf_columns = VCF_COLUMNS[:-2]

    info_fields = ("CLNSIG", "CLNDN")

    info_ann_fields = ("gene_name", "transcript_biotype", "effect", "impact")

    columns = vcf_columns + info_fields + info_ann_fields

    vcf_df_rows = []

    for i, variant_dict in enumerate(variant_dicts):

        if variant_dict["FILTER"] == "PASS":

            row = tuple(variant_dict[c] for c in vcf_columns) + tuple(
                variant_dict.get(field, nan) for field in info_fields
            )

            ann_dicts = variant_dict.get("ANN")

            if ann_dicts is not None:

                for ann_i, ann_dict in ann_dicts.items():

                    vcf_df_rows.append(
                        row
                        + tuple(ann_dict[ann_field] for ann_field in info_ann_fields)
                    )

    return (
        DataFrame(vcf_df_rows, columns=columns).drop_duplicates().set_index("gene_name")
    )
