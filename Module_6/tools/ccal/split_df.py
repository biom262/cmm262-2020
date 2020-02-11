def split_df(df, axis, n_split):

    if not (0 < n_split <= df.shape[axis]):

        raise ValueError(
            "Invalid: 0 < n_split ({}) <= n_slices ({})".format(n_split, df.shape[axis])
        )

    n = df.shape[axis] // n_split

    dfs = []

    for i in range(n_split):

        start_i = i * n

        end_i = (i + 1) * n

        if axis == 0:

            dfs.append(df.iloc[start_i:end_i])

        elif axis == 1:

            dfs.append(df.iloc[:, start_i:end_i])

    i = n * n_split

    if i < df.shape[axis]:

        if axis == 0:

            dfs.append(df.iloc[i:])

        elif axis == 1:

            dfs.append(df.iloc[:, i:])

    return dfs
