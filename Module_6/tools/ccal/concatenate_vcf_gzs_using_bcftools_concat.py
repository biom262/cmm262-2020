from os.path import dirname, isfile

from ._print_and_run_command import _print_and_run_command
from .bgzip_and_tabix import bgzip_and_tabix
from .get_function_name import get_function_name


def concatenate_vcf_gzs_using_bcftools_concat(
    vcf_gz_file_paths,
    remove_input_vcf_gz_file_paths_and_their_indices=False,
    n_job=1,
    output_vcf_file_path=None,
    overwrite=False,
):

    if output_vcf_file_path is None:

        output_vcf_file_path = "{}/{}.vcf".format(
            dirname(vcf_gz_file_paths[0]), get_function_name()
        )

    output_vcf_gz_file_path = "{}.gz".format(output_vcf_file_path)

    if not overwrite and isfile(output_vcf_gz_file_path):

        raise FileExistsError(output_vcf_gz_file_path)

    _print_and_run_command(
        "bcftools concat --allow-overlaps --threads {} {} > {}".format(
            n_job, " ".join(vcf_gz_file_paths), output_vcf_file_path
        )
    )

    if remove_input_vcf_gz_file_paths_and_their_indices:

        for vcf_gz_file_path in vcf_gz_file_paths:

            _print_and_run_command(
                "rm --recursive --force {0} {0}.tbi".format(vcf_gz_file_path)
            )

    return bgzip_and_tabix(output_vcf_file_path, n_job=n_job, overwrite=overwrite)
