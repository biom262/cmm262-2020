from os.path import dirname, isfile

from ._print_and_run_command import _print_and_run_command
from .get_function_name import get_function_name
from .index_bam_using_samtools_index import index_bam_using_samtools_index


def mark_duplicates_in_bam_using_picard_markduplicates(
    bam_file_path,
    memory="8G",
    remove_duplicates=False,
    remove_input_bam_file_path_and_its_index=False,
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

    metrics_file_path = "{}.metrics".format(output_bam_file_path)

    _print_and_run_command(
        "picard -Xmx{} MarkDuplicates REMOVE_DUPLICATES={} INPUT={} OUTPUT={} METRICS_FILE={}".format(
            memory,
            str(remove_duplicates).lower(),
            bam_file_path,
            output_bam_file_path,
            metrics_file_path,
        )
    )

    if remove_input_bam_file_path_and_its_index:

        _print_and_run_command(
            "rm --recursive --force {0} {0}.bai".format(bam_file_path)
        )

    print("{}:".format(metrics_file_path))

    with open(metrics_file_path) as metrics_file:

        print(metrics_file.read())

    return index_bam_using_samtools_index(
        output_bam_file_path, n_job=n_job, overwrite=overwrite
    )
