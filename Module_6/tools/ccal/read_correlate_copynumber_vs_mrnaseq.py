from tarfile import open as tarfile_open

from pandas import read_csv


def read_correlate_copynumber_vs_mrnaseq(tar_gz_file_path, genes):

    with tarfile_open(tar_gz_file_path) as tar_gz_file:

        n = read_csv(
            tar_gz_file.extractfile(
                tuple(file for file in tar_gz_file if file.name.endswith("qa.txt"))[0]
            ),
            sep="\t",
            index_col=0,
        ).loc["sample", "comm"]

        df = read_csv(
            tar_gz_file.extractfile(
                tuple(file for file in tar_gz_file if file.name.endswith("cors.txt"))[0]
            ),
            sep="\t",
            index_col=1,
        )

        return n, df.loc[genes, "cor"].to_dict()
