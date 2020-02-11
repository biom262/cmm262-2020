from pandas import read_csv


def read_gct(gct_file_path, drop_description=True):

    df = read_csv(gct_file_path, sep="\t", skiprows=2)

    column_0, column_1 = df.columns[:2]

    if column_0 == "Name":

        df.set_index("Name", inplace=True)

    else:

        raise ValueError("Column 0 != 'Name'.")

    if column_1 == "Description":

        if drop_description:

            df.drop("Description", axis=1, inplace=True)

    else:

        raise ValueError("Column 1 != 'Description'")

    return df
