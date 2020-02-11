from gzip import open as gzip_open
from shutil import copyfileobj, move


def gzip_compress_file(file_path):

    with open(file_path, mode="rb") as file:

        gzip_file_path = "{}.gz".format(file_path)

        gzip_file_path_temporary = "{}.temporary".format(gzip_file_path)

        with gzip_open(gzip_file_path_temporary, mode="wb") as gzip_file_temporary:

            copyfileobj(file, gzip_file_temporary)

    move(gzip_file_path_temporary, gzip_file_path)

    return gzip_file_path
