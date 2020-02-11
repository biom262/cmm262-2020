from os.path import isfile

from ._check_fastq_gzs import _check_fastq_gzs
from ._print_and_run_command import _print_and_run_command


def count_transcripts_using_kallisto_quant(
    fastq_gz_file_paths,
    fasta_gz_file_path,
    output_directory_path,
    n_bootstrap=0,
    fragment_length=180,
    fragment_length_standard_deviation=20,
    n_job=1,
    overwrite=False,
):

    _check_fastq_gzs(fastq_gz_file_paths)

    fasta_gz_kallisto_index_file_path = "{}.kallisto.index".format(fasta_gz_file_path)

    if not isfile(fasta_gz_kallisto_index_file_path):

        _print_and_run_command(
            "kallisto index --index {} {}".format(
                fasta_gz_kallisto_index_file_path, fasta_gz_file_path
            )
        )

    abundance_file_path = "{}/abundance.tsv".format(output_directory_path)

    if not overwrite and isfile(abundance_file_path):

        raise FileExistsError(abundance_file_path)

    if len(fastq_gz_file_paths) == 1:

        sample_argument = "--single --fragment-length {} --sd {} {}".format(
            fragment_length, fragment_length_standard_deviation, fastq_gz_file_paths[0]
        )

    elif len(fastq_gz_file_paths) == 2:

        sample_argument = "{} {}".format(*fastq_gz_file_paths)

    _print_and_run_command(
        "kallisto quant --index {} --output-dir {} --bootstrap-samples {} --threads {} {}".format(
            fasta_gz_kallisto_index_file_path,
            output_directory_path,
            n_bootstrap,
            n_job,
            sample_argument,
        )
    )

    return output_directory_path
