from numpy import asarray


def drop_df_slice(df, axis, max_na=None, min_n_not_na_unique_value=None):

    dropped = asarray((False,) * df.shape[(axis + 1) % 2])

    if max_na is not None:

        if max_na < 1:

            max_n_na = max_na * df.shape[axis]

        else:

            max_n_na = max_na

        dropped |= df.apply(lambda series: max_n_na < series.isna().sum(), axis=axis)

    if min_n_not_na_unique_value is not None:

        dropped |= df.apply(
            lambda series: series[~series.isna()].unique().size
            < min_n_not_na_unique_value,
            axis=axis,
        )

    if axis == 0:

        return df.loc[:, ~dropped]

    elif axis == 1:

        return df.loc[~dropped]
