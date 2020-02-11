from os.path import isfile

from .run_command import run_command


def establish_fai_index(fasta_gz_file_path):

    if not isfile("{}.fai".format(fasta_gz_file_path)):

        run_command("samtools faidx {}".format(fasta_gz_file_path), print_command=True)
