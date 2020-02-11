from os.path import isfile

from ._print_and_run_command import _print_and_run_command


def bgzip_and_tabix(file_path, n_job=1, overwrite=False):

    output_gz_file_path = "{}.gz".format(file_path)

    if not overwrite and isfile(output_gz_file_path):

        raise FileExistsError(output_gz_file_path)

    if overwrite:

        force = "--force"

    else:

        force = ""

    _print_and_run_command("bgzip --threads {} {} {}".format(n_job, force, file_path))

    _print_and_run_command("tabix {} {}".format(force, output_gz_file_path))

    return output_gz_file_path
