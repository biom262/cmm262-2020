from . import DATA_DIRECTORY_PATH

GENERAL_BAD_SEQUENCES_FILE_PATH = "{}/general_bad_sequences.fasta".format(
    DATA_DIRECTORY_PATH
)


def _check_fastq_gzs(fastq_gz_file_paths):

    if len(fastq_gz_file_paths) not in (1, 2):

        raise ValueError(
            "fastq_gz_file_paths should contain either 1 (unpaired) or 2 (paired) .fastq.gz file path(s)."
        )
