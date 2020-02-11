from os.path import dirname, isfile

from ._print_and_run_command import _print_and_run_command
from .get_function_name import get_function_name
from .index_bam_using_samtools_index import index_bam_using_samtools_index


def sort_and_index_bam_using_samtools_sort_and_index(
    bam_file_path,
    remove_input_bam_file_path=False,
    n_job=1,
    output_bam_file_path=None,
    overwrite=False,
):

    if output_bam_file_path is None:

        output_bam_file_path = "{}/{}.bam".format(
            dirname(bam_file_path), get_function_name()
        )

    if not overwrite and isfile(output_bam_file_path):

        raise FileExistsError(output_bam_file_path)

    _print_and_run_command(
        "samtools sort --threads {} {} > {}".format(
            n_job, bam_file_path, output_bam_file_path
        )
    )

    if remove_input_bam_file_path:

        _print_and_run_command("rm --recursive --force {}".format(bam_file_path))

    return index_bam_using_samtools_index(
        output_bam_file_path, n_job=n_job, overwrite=overwrite
    )
