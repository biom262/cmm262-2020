from gzip import open as gzip_open
from shutil import copyfileobj, move


def gzip_decompress_file(gzip_file_path):

    with gzip_open(gzip_file_path, mode="rt") as gzip_file:

        file_path = gzip_file_path[: -len(".gz")]

        file_path_temporary = "{}.temporary".format(file_path)

        with open(file_path_temporary, mode="wt") as file_temporary:

            copyfileobj(gzip_file, file_temporary)

    move(file_path_temporary, file_path)

    return file_path
