from os.path import isfile

from . import DATA_DIRECTORY_PATH
from ._print_and_run_command import _print_and_run_command

GENERAL_BAD_SEQUENCES_FILE_PATH = "{}/general_bad_sequences.fasta".format(
    DATA_DIRECTORY_PATH
)


def check_fastq_gzs_using_fastqc(fastq_gz_file_paths, n_job=1, overwrite=False):

    for fastq_gz_file_path in fastq_gz_file_paths:

        html_file_path = "{}_fastqc.html".format(fastq_gz_file_path)

        if not overwrite and isfile(html_file_path):

            raise FileExistsError(html_file_path)

    _print_and_run_command(
        "fastqc --threads {} {}".format(n_job, " ".join(fastq_gz_file_paths))
    )
