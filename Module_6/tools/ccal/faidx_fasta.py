from ._print_and_run_command import _print_and_run_command


def faidx_fasta(fasta_file_path):

    _print_and_run_command("samtools faidx {}".format(fasta_file_path))
