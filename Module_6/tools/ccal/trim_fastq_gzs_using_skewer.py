from os.path import dirname, isdir

from . import DATA_DIRECTORY_PATH
from ._check_fastq_gzs import _check_fastq_gzs
from ._gzip_compress import _gzip_compress
from ._print_and_run_command import _print_and_run_command
from .get_function_name import get_function_name
from .multiprocess import multiprocess

GENERAL_BAD_SEQUENCES_FILE_PATH = "{}/general_bad_sequences.fasta".format(
    DATA_DIRECTORY_PATH
)


def trim_fastq_gzs_using_skewer(
    fastq_gz_file_paths,
    forward_bad_sequences_fasta_file_path=GENERAL_BAD_SEQUENCES_FILE_PATH,
    reverse_bad_sequences_fasta_file_path=GENERAL_BAD_SEQUENCES_FILE_PATH,
    snv_error_rate=0,
    indel_error_rate=0,
    overlap_length=12,
    end_quality=30,
    min_length_after_trimming=30,
    remove_n=True,
    n_job=1,
    output_directory_path=None,
    overwrite=False,
):

    _check_fastq_gzs(fastq_gz_file_paths)

    if output_directory_path is None:

        output_directory_path = "{}/{}".format(
            dirname(fastq_gz_file_paths[0]), get_function_name()
        )

    if not output_directory_path.endswith("/"):

        output_directory_path += "/"

    if not overwrite and isdir(output_directory_path):

        raise FileExistsError(output_directory_path)

    additional_arguments = []

    if len(fastq_gz_file_paths) == 1:

        additional_arguments.append("-m tail")

        additional_arguments.append("-k {}".format(overlap_length))

    elif len(fastq_gz_file_paths) == 2:

        additional_arguments.append("-m pe")

        additional_arguments.append(
            "-y {}".format(reverse_bad_sequences_fasta_file_path)
        )

    if remove_n:

        remove_n = "-n"

    else:

        remove_n = ""

    _print_and_run_command(
        "skewer -x {} -r {} -d {} --end-quality {} --min {} {} --output {} --masked-output --excluded-output --threads {} {}".format(
            forward_bad_sequences_fasta_file_path,
            snv_error_rate,
            indel_error_rate,
            end_quality,
            min_length_after_trimming,
            remove_n,
            output_directory_path,
            n_job,
            " ".join(additional_arguments + list(fastq_gz_file_paths)),
        )
    )

    log_file_path = "{}/trimmed.log".format(output_directory_path)

    print("{}:".format(log_file_path))

    with open(log_file_path) as log_file:

        print(log_file.read())

    return multiprocess(
        _gzip_compress,
        (
            (outptu_fastq_file_path,)
            for outptu_fastq_file_path in (
                "{}/trimmed-pair{}.fastq".format(output_directory_path, i)
                for i in (1, 2)
            )
        ),
        n_job=n_job,
    )
