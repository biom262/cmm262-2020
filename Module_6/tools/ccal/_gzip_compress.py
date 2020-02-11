from ._print_and_run_command import _print_and_run_command


def _gzip_compress(file_path):

    _print_and_run_command("gzip --force {}".format(file_path))

    return "{}.gz".format(file_path)
