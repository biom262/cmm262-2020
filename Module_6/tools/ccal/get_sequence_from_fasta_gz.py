from .establish_fai_index import establish_fai_index
from .run_command import run_command


def get_sequence_from_fasta_gz(
    fasta_gz_file_path, chromosome, start_position, end_position
):

    establish_fai_index(fasta_gz_file_path)

    return "".join(
        run_command(
            "samtools faidx {} {}:{}-{}".format(
                fasta_gz_file_path, chromosome, start_position, end_position
            ),
            print_command=True,
        )
        .stdout.strip()
        .split(sep="\n")[1:]
    )
