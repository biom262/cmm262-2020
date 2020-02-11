def sample_series_randomly_per_value(series, n_per_value=None, random_seed=20121020):

    if n_per_value is None:

        n_per_value = series.value_counts().min()

        print("n_per_value = {}".format(n_per_value))

    indices_selected = []

    for group_name, group_series in series.groupby(series):

        if n_per_value <= group_series.size:

            indices_selected.extend(
                group_series.sample(
                    n=n_per_value, random_state=random_seed
                ).index.sort_values()
            )

        else:

            print("Not sampling {}; N < {}.".format(group_name, n_per_value))

    return series[indices_selected]
