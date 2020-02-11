from numpy import asarray
from pandas import DataFrame

from .apply_function_on_2_2d_arrays_slices import apply_function_on_2_2d_arrays_slices
from .compute_information_coefficient import compute_information_coefficient
from .plot_heat_map import plot_heat_map


def make_comparison_panel(
    _2d_array_or_df_0,
    _2d_array_or_df_1,
    match_function=compute_information_coefficient,
    axis=0,
    title=None,
    name_0=None,
    name_1=None,
    file_path_prefix=None,
    plotly_html_file_path_prefix=None,
):

    comparison = apply_function_on_2_2d_arrays_slices(
        asarray(_2d_array_or_df_0), asarray(_2d_array_or_df_1), match_function, axis
    )

    if isinstance(_2d_array_or_df_0, DataFrame) and isinstance(
        _2d_array_or_df_1, DataFrame
    ):

        if axis == 0:

            comparison = DataFrame(
                comparison,
                index=_2d_array_or_df_0.columns,
                columns=_2d_array_or_df_1.columns,
            )

        elif axis == 1:

            comparison = DataFrame(
                comparison,
                index=_2d_array_or_df_0.index,
                columns=_2d_array_or_df_1.index,
            )

    if file_path_prefix is None:

        html_file_path = None

    else:

        comparison.to_csv("{}.tsv".format(file_path_prefix), sep="\t")

        html_file_path = "{}.html".format(file_path_prefix)

    if plotly_html_file_path_prefix is None:

        plotly_html_file_path = None

    else:

        plotly_html_file_path = "{}.html".format(plotly_html_file_path_prefix)

    plot_heat_map(
        comparison,
        cluster_axis="01",
        title=title,
        xaxis_title=name_1,
        yaxis_title=name_0,
        html_file_path=html_file_path,
        plotly_html_file_path=plotly_html_file_path,
    )

    return comparison
