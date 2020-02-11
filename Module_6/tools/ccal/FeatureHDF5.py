from collections import defaultdict
from gzip import open as gzip_open
from pickle import dump, load
from warnings import warn

from tables import Filters, HDF5ExtError, Int32Col, IsDescription, StringCol, open_file

from .read_where_and_map_column_names import read_where_and_map_column_names


class FeatureHDF5:
    def __init__(self, gff3_gz_file_path, types=("gene",), reset=False):

        self._gff3_gz_file_path = gff3_gz_file_path

        self._feature_hdf5_file_path = "{}.hdf5".format(self._gff3_gz_file_path)

        self._name_seqid_pickle_gz_file_path = "{}.name_seqid.pickle.gz".format(
            self._gff3_gz_file_path
        )

        self._types = types

        self._feature_hdf5 = None

        self._name_seqid = {}

        self._initialize(reset=reset)

    def __del__(self):

        if self._feature_hdf5:

            self._feature_hdf5.close()

            print("Destructor closed {}.".format(self._feature_hdf5_file_path))

    def _initialize(self, reset=False):

        if not reset:

            try:

                print("Initializing FeatureHDF5 ...")

                print("\tReading {} ...".format(self._feature_hdf5_file_path))

                self._feature_hdf5 = open_file(self._feature_hdf5_file_path)

                print("\tReading {} ...".format(self._name_seqid_pickle_gz_file_path))

                with gzip_open(
                    self._name_seqid_pickle_gz_file_path
                ) as name_seqid_pickle_gz_file:

                    self._name_seqid = load(name_seqid_pickle_gz_file)

            except (OSError, FileNotFoundError, HDF5ExtError) as exception:

                warn("\tFailed: {}.".format(exception))

                reset = True

        if reset:

            print("Resetting ...")

            if self._feature_hdf5:

                self._feature_hdf5.close()

                print("\tClosed {} ...".format(self._feature_hdf5_file_path))

            print("\tMaking {} ...".format(self._feature_hdf5_file_path))

            self._make_feature_hdf5()

            print("\tReading {} ...".format(self._feature_hdf5_file_path))

            self._feature_hdf5 = open_file(self._feature_hdf5_file_path)

    def _make_feature_hdf5(self):

        with gzip_open(self._gff3_gz_file_path) as gff3_gz_file:

            print("Getting data-start position ...")

            data_start_position = None

            line = gff3_gz_file.readline().decode()

            while line.startswith("#"):

                data_start_position = gff3_gz_file.tell()

                line = gff3_gz_file.readline().decode()

            print("Counting features per seqid ...")

            seqid_n_row = defaultdict(lambda: 0)

            n = 0

            seqid = None

            while line:

                n += 1

                if not line.startswith("#"):

                    seqid_ = line.split(sep="\t")[0]

                    if seqid_ != seqid:

                        print("\t{} ...".format(seqid_))

                        seqid = seqid_

                    seqid_n_row[seqid_] += 1

                line = gff3_gz_file.readline().decode()

            print("Making {} ...".format(self._feature_hdf5_file_path))

            with open_file(
                self._feature_hdf5_file_path,
                mode="w",
                filters=Filters(complevel=1, complib="blosc"),
            ) as feature_hdf5:

                seqid_table_row = {}

                n_per_print = max(1, n // 10)

                gff3_gz_file.seek(data_start_position)

                for i, line in enumerate(gff3_gz_file):

                    if i % n_per_print == 0:

                        print("\t{:,}/{:,} ...".format(i, n))

                    line = line.decode(errors="replace")

                    if line.startswith("#"):

                        continue

                    seqid, source, type_, start, end, score, strand, phase, attributes = line.split(
                        "\t"
                    )

                    if type_ not in self._types:

                        continue

                    if seqid not in seqid_table_row:

                        print("\t\tMaking {} table ...".format(seqid))

                        seqid_table = feature_hdf5.create_table(
                            "/",
                            "seqid_{}_features".format(seqid),
                            description=self._FeatureDescription,
                            expectedrows=seqid_n_row[seqid],
                        )

                        seqid_table_row[seqid] = seqid_table.row

                    cursor = seqid_table_row[seqid]

                    cursor["seqid"] = seqid

                    cursor["start"] = start

                    cursor["end"] = end

                    name = None

                    biotype = None

                    for attribute in attributes.split(sep=";"):

                        field, value = attribute.split(sep="=")

                        if field == "Name":

                            name = value

                        elif field == "biotype":

                            biotype = value

                    cursor["Name"] = name

                    cursor["biotype"] = biotype

                    cursor.append()

                    self._name_seqid[name] = seqid

                print("\tFlushing tables and making column indices ...")

                for seqid in seqid_table_row:

                    print("\t\t{} table ...".format(seqid))

                    seqid_table = feature_hdf5.get_node(
                        "/", "seqid_{}_features".format(seqid)
                    )

                    seqid_table.flush()

                    for column in ("seqid", "start", "end", "Name", "biotype"):

                        seqid_table.cols._f_col(column).create_csindex()

                self._feature_hdf5 = feature_hdf5

                print(self._feature_hdf5)

                print("Writing {} ...".format(self._name_seqid_pickle_gz_file_path))

                with gzip_open(
                    self._name_seqid_pickle_gz_file_path, mode="wb"
                ) as name_seqid_pickle_gz_file:

                    dump(self._name_seqid, name_seqid_pickle_gz_file)

    class _FeatureDescription(IsDescription):

        seqid = StringCol(256)

        start = Int32Col()

        end = Int32Col()

        Name = StringCol(256)

        biotype = StringCol(256)

    def get_features_by_name(self, name):

        seqid = self._name_seqid[name]

        seqid_table = self._feature_hdf5.get_node(
            "/", "seqid_{}_features".format(seqid)
        )

        feature_dicts = read_where_and_map_column_names(
            seqid_table, "Name == b'{}'".format(name)
        )

        return feature_dicts

    def get_features_by_region(self, seqid, start_position, end_position):

        seqid_table = self._feature_hdf5.get_node(
            "/", "seqid_{}_features".format(seqid)
        )

        feature_dicts = read_where_and_map_column_names(
            seqid_table,
            "({} <= start) & (end <= {})".format(start_position, end_position),
        )

        return feature_dicts
