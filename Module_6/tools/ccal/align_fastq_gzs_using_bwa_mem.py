from os.path import dirname, isfile
from sys import platform

from . import DATA_DIRECTORY_PATH
from ._check_fastq_gzs import _check_fastq_gzs
from ._print_and_run_command import _print_and_run_command
from .get_function_name import get_function_name

GENERAL_BAD_SEQUENCES_FILE_PATH = "{}/general_bad_sequences.fasta".format(
    DATA_DIRECTORY_PATH
)


def align_fastq_gzs_using_bwa_mem(
    fastq_gz_file_paths,
    fasta_gz_file_path,
    n_job=1,
    output_bam_file_path=None,
    overwrite=False,
):

    _check_fastq_gzs(fastq_gz_file_paths)

    if not all(
        isfile("{}{}".format(fasta_gz_file_path, file_extension))
        for file_extension in (".bwt", ".pac", ".ann", ".amb", ".sa")
    ):

        _print_and_run_command("bwa index {}".format(fasta_gz_file_path))

    if not isfile("{}.alt".format(fasta_gz_file_path)):

        raise FileNotFoundError(
            "ALT-aware BWA-MEM alignment needs {}.alt.".format(fasta_gz_file_path)
        )

    if output_bam_file_path is None:

        output_bam_file_path = "{}/{}.bam".format(
            dirname(fastq_gz_file_paths[0]), get_function_name()
        )

    if not overwrite and isfile(output_bam_file_path):

        raise FileExistsError(output_bam_file_path)

    _print_and_run_command(
        "bwa mem -t {0} -v 3 {1} {2} | {3}/k8-0.2.3/k8-{4} {3}/bwa-postalt.js {5}.alt | samtools view -Sb --threads {1} > {6}".format(
            n_job,
            fasta_gz_file_path,
            " ".join(fastq_gz_file_paths),
            DATA_DIRECTORY_PATH,
            platform,
            fasta_gz_file_path,
            output_bam_file_path,
        )
    )

    return output_bam_file_path
