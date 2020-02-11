from numpy import nan

from .drop_df_slice_greedily import drop_df_slice_greedily


def clean_and_write_df_to_tsv(df, index_name, tsv_file_path):

    assert not df.index.hasnans

    assert not df.columns.hasnans

    assert not df.index.has_duplicates

    assert not df.columns.has_duplicates

    df = df.fillna(nan)

    df = drop_df_slice_greedily(df, min_n_not_na_unique_value=1)

    df = df.sort_index().sort_index(axis=1)

    df.index.name = index_name

    df.to_csv(tsv_file_path, sep="\t")

    return df
