from os.path import dirname, isfile

from . import DATA_DIRECTORY_PATH
from ._check_fastq_gzs import _check_fastq_gzs
from ._print_and_run_command import _print_and_run_command
from .get_function_name import get_function_name

GENERAL_BAD_SEQUENCES_FILE_PATH = "{}/general_bad_sequences.fasta".format(
    DATA_DIRECTORY_PATH
)


def align_fastq_gzs_using_hisat2(
    fastq_gz_file_paths,
    fasta_file_path,
    sequence_type,
    n_job=1,
    output_bam_file_path=None,
    overwrite=False,
):

    _check_fastq_gzs(fastq_gz_file_paths)

    if not all(
        isfile("{}.{}.ht2".format(fasta_file_path, i)) for i in (1, 2, 3, 4, 5, 6, 7, 8)
    ):

        _print_and_run_command("hisat2-build {0} {0}".format(fasta_file_path))

    if output_bam_file_path is None:

        output_bam_file_path = "{}/{}.bam".format(
            dirname(fastq_gz_file_paths[0]), get_function_name()
        )

    if not overwrite and isfile(output_bam_file_path):

        raise FileExistsError(output_bam_file_path)

    additional_arguments = []

    if len(fastq_gz_file_paths) == 1:

        additional_arguments.append("-U {}".format(fastq_gz_file_paths[0]))

    elif len(fastq_gz_file_paths) == 2:

        additional_arguments.append("-1 {} -2 {}".format(*fastq_gz_file_paths))

    if sequence_type not in ("DNA", "RNA"):

        raise ValueError("Unknown sequence_type: {}.".format(sequence_type))

    elif sequence_type == "DNA":

        additional_arguments.append("--no-spliced-alignment")

    elif sequence_type == "RNA":

        additional_arguments.append("--dta --dta-cufflinks")

    _print_and_run_command(
        "hisat2 -x {0} --summary-file {1}.summary --threads {2} {3} | samtools view -Sb --threads {2} > {1}".format(
            fasta_file_path, output_bam_file_path, n_job, " ".join(additional_arguments)
        )
    )

    return output_bam_file_path
