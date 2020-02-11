from warnings import warn


def write_gct(df, gct_file_path, descriptions=None):

    df = df.copy()

    if df.columns[0] != "Description":

        if descriptions is not None:

            df.insert(0, "Description", descriptions)

        else:

            df.insert(0, "Description", df.index)

    df.index.name = "Name"

    df.columns.name = None

    if not gct_file_path.endswith(".gct"):

        warn("Adding '.gct' to {} ...".format(gct_file_path))

        gct_file_path += ".gct"

    with open(gct_file_path, mode="w") as gct_file:

        gct_file.writelines("#1.2\n{}\t{}\n".format(df.shape[0], df.shape[1] - 1))

        df.to_csv(gct_file, sep="\t")
