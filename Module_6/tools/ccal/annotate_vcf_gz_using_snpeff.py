from os.path import dirname, isfile

from ._print_and_run_command import _print_and_run_command
from .bgzip_and_tabix import bgzip_and_tabix
from .get_function_name import get_function_name


def annotate_vcf_gz_using_snpeff(
    vcf_gz_file_path,
    genomic_assembly,
    memory="8G",
    remove_input_vcf_gz_file_path_and_its_index=False,
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

    _print_and_run_command(
        "snpEff -Xmx{0} -htmlStats {1}.stats.html -csvStats {1}.stats.csv -t -verbose -noLog {2} {3} > {1}".format(
            memory, output_vcf_file_path, genomic_assembly, vcf_gz_file_path
        )
    )

    if remove_input_vcf_gz_file_path_and_its_index:

        _print_and_run_command(
            "rm --recursive --force {0} {0}.tbi".format(vcf_gz_file_path)
        )

    return bgzip_and_tabix(output_vcf_file_path, n_job=n_job, overwrite=overwrite)
