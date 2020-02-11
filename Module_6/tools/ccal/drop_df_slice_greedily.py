from .drop_df_slice import drop_df_slice


def drop_df_slice_greedily(df, max_na=None, min_n_not_na_unique_value=None):

    shift = int(df.shape[1] < df.shape[0])

    for i in range(df.size):

        shape_before = df.shape

        axis = (i + shift) % 2

        df = drop_df_slice(
            df, axis, max_na=max_na, min_n_not_na_unique_value=min_n_not_na_unique_value
        )

        shape_after = df.shape

        print("Shape: {} =(drop axis {})=> {}".format(shape_before, axis, shape_after))

        if 0 < i and shape_before == shape_after:

            return df
