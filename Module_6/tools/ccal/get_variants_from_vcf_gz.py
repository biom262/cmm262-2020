from tabix import open as tabix_open

from .parse_vcf_row_and_make_variant_dict import parse_vcf_row_and_make_variant_dict
from .update_variant_dict import update_variant_dict


def get_variants_from_vcf_gz(
    chromosome, start_position, end_position, pytabix_handle=None, vcf_gz_file_path=None
):

    if pytabix_handle is None:

        if vcf_gz_file_path is None:

            raise ValueError("Provide either pytabix_handle or vcf_gz_file_path.")

        else:

            pytabix_handle = tabix_open(vcf_gz_file_path)

    variants = pytabix_handle.query(chromosome, start_position, end_position)

    varinat_dicts = [
        parse_vcf_row_and_make_variant_dict(variant) for variant in variants
    ]

    for variant_dict in varinat_dicts:

        update_variant_dict(variant_dict)

    return varinat_dicts
