from os.path import isfile

from ._print_and_run_command import _print_and_run_command


def check_bam_using_samtools_flagstat(bam_file_path, n_job=1, overwrite=False):

    flagstat_file_path = "{}.flagstat".format(bam_file_path)

    if not overwrite and isfile(flagstat_file_path):

        raise FileExistsError(flagstat_file_path)

    _print_and_run_command(
        "samtools flagstat --threads {} {} > {}".format(
            n_job, bam_file_path, flagstat_file_path
        )
    )

    print("{}:".format(flagstat_file_path))

    with open(flagstat_file_path) as flagstat_file:

        print(flagstat_file.read())
