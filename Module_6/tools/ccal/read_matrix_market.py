from pandas import DataFrame, read_csv
from scipy.io import mmread


def read_matrix_market(
    matrix_mtx_file_path,
    index_file_path,
    column_file_path,
    index_name=None,
    column_name=None,
):

    df = DataFrame(
        mmread(matrix_mtx_file_path).toarray(),
        index=read_csv(index_file_path, sep="\t", header=None).iloc[:, -1],
        columns=read_csv(column_file_path, sep="\t", header=None, squeeze=True),
    )

    if df.index.has_duplicates:

        print("Index duplicated. Merging duplicates ...")

        df = df.groupby(level=0).max()

    df.sort_index(inplace=True)

    df.index.name = index_name

    if df.columns.has_duplicates:

        print("Column duplicated. Merging duplicates ...")

        df = df.T.groupby(level=0).max().T

    df.sort_index(axis=1, inplace=True)

    df.columns.name = column_name

    return df
