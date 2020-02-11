from os.path import dirname, isfile

from ._print_and_run_command import _print_and_run_command
from .bgzip_and_tabix import bgzip_and_tabix
from .get_function_name import get_function_name


def get_variants_from_bam_using_freebayes(
    bam_file_path,
    fasta_file_path,
    regions=None,
    n_job=1,
    output_vcf_file_path=None,
    overwrite=False,
):

    if output_vcf_file_path is None:

        output_vcf_file_path = "{}/{}.vcf".format(
            dirname(bam_file_path), get_function_name()
        )

    additional_arguments = []

    if regions is not None:

        additional_arguments.append("--region {}".format(regions))

    if len(additional_arguments):

        output_vcf_file_path = output_vcf_file_path.replace(
            ".vcf", ".{}.vcf".format(" ".join(additional_arguments).replace(" ", "_"))
        )

    output_vcf_gz_file_path = "{}.gz".format(output_vcf_file_path)

    if not overwrite and isfile(output_vcf_gz_file_path):

        raise FileExistsError(output_vcf_gz_file_path)

    _print_and_run_command(
        "freebayes --fasta-reference {} {} {} > {}".format(
            fasta_file_path,
            " ".join(additional_arguments),
            bam_file_path,
            output_vcf_file_path,
        )
    )

    return bgzip_and_tabix(output_vcf_file_path, n_job=n_job, overwrite=overwrite)
