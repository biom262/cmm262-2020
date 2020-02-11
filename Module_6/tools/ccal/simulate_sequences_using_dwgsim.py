from ._print_and_run_command import _print_and_run_command
from .bgzip_and_tabix import bgzip_and_tabix


def simulate_sequences_using_dwgsim(
    fasta_file_path,
    output_file_path_prefix,
    n_sequence=1e3,
    fraction_variant=1e-3,
    fraction_indel_variant=1e-1,
):

    _print_and_run_command(
        "dwgsim -N {} -1 150 -2 150 -r {} -R {} {} {}".format(
            n_sequence,
            fraction_variant,
            fraction_indel_variant,
            fasta_file_path,
            output_file_path_prefix,
        )
    )

    for read_id in (1, 2):

        _print_and_run_command(
            "gzip {}.bwa.read{}.fastq".format(output_file_path_prefix, read_id)
        )

    _print_and_run_command(
        "rm --recursive --force {}.bfast.fastq".format(output_file_path_prefix)
    )

    bgzip_and_tabix("{}.mutations.vcf".format(output_file_path_prefix))
