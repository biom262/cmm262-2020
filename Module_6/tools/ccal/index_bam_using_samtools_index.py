from os.path import isfile

from ._print_and_run_command import _print_and_run_command


def index_bam_using_samtools_index(bam_file_path, n_job=1, overwrite=False):

    output_bam_bai_file_path = "{}.bai".format(bam_file_path)

    if not overwrite and isfile(output_bam_bai_file_path):

        raise FileExistsError(output_bam_bai_file_path)

    _print_and_run_command("samtools index -@ {} {}".format(n_job, bam_file_path))

    return bam_file_path
