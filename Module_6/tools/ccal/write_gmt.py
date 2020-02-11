from warnings import warn


def write_gmt(df, gmt_file_path, descriptions=None):

    df = df.copy()

    if df.columns[0] != "Description":

        if descriptions is not None:

            df.insert(0, "Description", descriptions)

        else:

            df.insert(0, "Description", df.index)

    if not gmt_file_path.endswith(".gmt"):

        warn("Adding .gmt to {} ...".format(gmt_file_path))

        gmt_file_path += ".gmt"

    df.to_csv(gmt_file_path, header=None, sep="\t")
