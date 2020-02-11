from os.path import dirname, isfile

from ._print_and_run_command import _print_and_run_command
from .bgzip_and_tabix import bgzip_and_tabix
from .get_function_name import get_function_name


def filter_vcf_gz_using_bcftools_view(
    vcf_gz_file_path,
    regions=None,
    keep_filters=None,
    include_expression=None,
    n_job=1,
    output_vcf_file_path=None,
    overwrite=False,
):

    if output_vcf_file_path is None:

        output_vcf_file_path = "{}/{}.vcf".format(
            dirname(vcf_gz_file_path), get_function_name()
        )

    output_vcf_gz_file_path = "{}.gz".format(output_vcf_file_path)

    if not overwrite and isfile(output_vcf_gz_file_path):

        raise FileExistsError(output_vcf_gz_file_path)

    additional_arguments = []

    if regions is not None:

        additional_arguments.append("--regions {}".format(",".join(regions)))

    if keep_filters is not None:

        additional_arguments.append("--apply-filters {}".format(",".join(keep_filters)))

    if include_expression is not None:

        additional_arguments.append("--include '{}'".format(include_expression))

    _print_and_run_command(
        "bcftools view {} --threads {} {} > {}".format(
            " ".join(additional_arguments),
            n_job,
            vcf_gz_file_path,
            output_vcf_file_path,
        )
    )

    return bgzip_and_tabix(output_vcf_file_path, n_job=n_job, overwrite=overwrite)
