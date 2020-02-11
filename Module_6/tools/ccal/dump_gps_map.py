from gzip import open as gzip_open
from pickle import dump


def dump_gps_map(gps_map, pickle_gz_file_path):

    if not pickle_gz_file_path.endswith(".pickle.gz"):

        pickle_gz_file_path += ".pickle.gz"

    with gzip_open(pickle_gz_file_path, mode="wb") as pickle_gz_file:

        dump(gps_map, pickle_gz_file)
