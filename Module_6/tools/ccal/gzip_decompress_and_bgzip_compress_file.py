from gzip import open as gzip_open
from shutil import copyfileobj, move

from Bio.bgzf import open as bgzf_open


def gzip_decompress_and_bgzip_compress_file(gzip_file_path):

    with gzip_open(gzip_file_path) as gzip_file:

        bgzip_file_path = gzip_file_path

        bgzip_file_path_temporary = "{}.temporary".format(bgzip_file_path)

        with bgzf_open(bgzip_file_path_temporary, mode="wb") as bgzip_file_temporary:

            copyfileobj(gzip_file, bgzip_file_temporary)

    move(bgzip_file_path_temporary, bgzip_file_path)

    return bgzip_file_path
