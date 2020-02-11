from .plot_and_save import plot_and_save


def select_series_indices(
    series,
    direction,
    threshold=None,
    n=None,
    fraction=None,
    standard_deviation=None,
    plot=True,
    title=None,
    xaxis=None,
    yaxis=None,
    html_file_path=None,
    plotly_file_path=None,
):

    series_sorted = series.dropna().sort_values()

    if n is not None:

        if direction in ("<", ">"):

            n = min(n, series_sorted.size)

        elif direction == "<>":

            n = min(n, series_sorted.size // 2)

    if fraction is not None:

        if direction in ("<", ">"):

            fraction = min(fraction, 1)

        elif direction == "<>":

            fraction = min(fraction, 1 / 2)

    if direction == "<":

        if threshold is None:

            if n is not None:

                threshold = series_sorted.iloc[n]

            elif fraction is not None:

                threshold = series_sorted.quantile(fraction)

            elif standard_deviation is not None:

                threshold = (
                    series_sorted.mean() - series_sorted.std() * standard_deviation
                )

        is_selected = series_sorted <= threshold

    elif direction == ">":

        if threshold is None:

            if n is not None:

                threshold = series_sorted.iloc[-n]

            elif fraction is not None:

                threshold = series_sorted.quantile(1 - fraction)

            elif standard_deviation is not None:

                threshold = (
                    series_sorted.mean() + series_sorted.std() * standard_deviation
                )

        is_selected = threshold <= series_sorted

    elif direction == "<>":

        if n is not None:

            threshold_low = series_sorted.iloc[n]

            threshold_high = series_sorted.iloc[-n]

        elif fraction is not None:

            threshold_low = series_sorted.quantile(fraction)

            threshold_high = series_sorted.quantile(1 - fraction)

        elif standard_deviation is not None:

            threshold_low = (
                series_sorted.mean() - series_sorted.std() * standard_deviation
            )

            threshold_high = (
                series_sorted.mean() + series_sorted.std() * standard_deviation
            )

        is_selected = (series_sorted <= threshold_low) | (
            threshold_high <= series_sorted
        )

    if plot:

        plot_and_save(
            dict(
                layout=dict(title=title, xaxis=xaxis, yaxis=yaxis),
                data=[
                    dict(
                        type="scatter",
                        name="All",
                        x=tuple(range(series_sorted.size)),
                        y=series_sorted,
                        text=series_sorted.index,
                        mode="markers",
                        marker=dict(color="#20d9ba"),
                    ),
                    dict(
                        type="scatter",
                        name="Selected",
                        x=is_selected.nonzero()[0],
                        y=series_sorted[is_selected],
                        text=series_sorted.index[is_selected],
                        mode="markers",
                        marker=dict(color="#9017e6"),
                    ),
                ],
            ),
            html_file_path,
            plotly_file_path,
        )

    return series_sorted.index[is_selected]
