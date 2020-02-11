from ._make_annotations import _make_annotations
from ._match import _match
from ._process_target_or_data_for_plotting import _process_target_or_data_for_plotting
from .cluster_2d_array_slices import cluster_2d_array_slices
from .compute_information_coefficient import compute_information_coefficient
from .nd_array_is_sorted import nd_array_is_sorted
from .plot_and_save import plot_and_save
from .select_series_indices import select_series_indices


def make_match_panel(
    target,
    data,
    target_ascending=True,
    score_moe_p_value_fdr=None,
    n_job=1,
    match_function=compute_information_coefficient,
    n_required_for_match_function=2,
    raise_for_n_less_than_required=False,
    n_extreme=8,
    fraction_extreme=None,
    random_seed=20_121_020,
    n_sampling=0,
    n_permutation=0,
    score_ascending=False,
    plot_only_sign=None,
    target_type="continuous",
    cluster_within_category=True,
    data_type="continuous",
    plot_std=None,
    title=None,
    layout_width=880,
    row_height=64,
    layout_side_margin=196,
    annotation_font_size=10,
    file_path_prefix=None,
    plotly_html_file_path_prefix=None,
):

    common_indices = target.index & data.columns

    print(
        "target.index ({}) & data.columns ({}) have {} in common.".format(
            target.index.size, data.columns.size, len(common_indices)
        )
    )

    target = target[common_indices]

    if target_ascending is not None:

        target.sort_values(ascending=target_ascending, inplace=True)

    data = data[target.index]

    if score_moe_p_value_fdr is None:

        score_moe_p_value_fdr = _match(
            target.values,
            data.values,
            n_job,
            match_function,
            n_required_for_match_function,
            raise_for_n_less_than_required,
            n_extreme,
            fraction_extreme,
            random_seed,
            n_sampling,
            n_permutation,
        )

        if score_moe_p_value_fdr.isna().values.all():

            return score_moe_p_value_fdr

        score_moe_p_value_fdr.index = data.index

        score_moe_p_value_fdr.sort_values(
            "Score", ascending=score_ascending, inplace=True
        )

        if file_path_prefix is not None:

            score_moe_p_value_fdr.to_csv("{}.tsv".format(file_path_prefix), sep="\t")

    else:

        score_moe_p_value_fdr = score_moe_p_value_fdr.reindex(index=data.index)

    scores_to_plot = score_moe_p_value_fdr.copy()

    if n_extreme is not None or fraction_extreme is not None:

        scores_to_plot = score_moe_p_value_fdr.loc[
            select_series_indices(
                score_moe_p_value_fdr["Score"],
                "<>",
                n=n_extreme,
                fraction=fraction_extreme,
                plot=False,
            )
        ]

    if plot_only_sign is not None:

        if plot_only_sign == "-":

            indices = scores_to_plot["Score"] <= 0

        elif plot_only_sign == "+":

            indices = 0 <= scores_to_plot["Score"]

        scores_to_plot = scores_to_plot.loc[indices]

    scores_to_plot.sort_values("Score", ascending=score_ascending, inplace=True)

    data_to_plot = data.loc[scores_to_plot.index]

    annotations = _make_annotations(scores_to_plot)

    target, target_plot_min, target_plot_max, target_colorscale = _process_target_or_data_for_plotting(
        target, target_type, plot_std
    )

    if (
        cluster_within_category
        and target_type in ("binary", "categorical")
        and 1 < target.value_counts().min()
        and nd_array_is_sorted(target.values)
        and not data_to_plot.isna().all().any()
    ):

        print("Clustering heat map within category ...")

        clustered_indices = cluster_2d_array_slices(
            data_to_plot.values, 1, groups=target.values, raise_for_bad=False
        )

        target = target.iloc[clustered_indices]

        data_to_plot = data_to_plot.iloc[:, clustered_indices]

    data_to_plot, data_plot_min, data_plot_max, data_colorscale = _process_target_or_data_for_plotting(
        data_to_plot, data_type, plot_std
    )

    target_row_fraction = max(0.01, 1 / (data_to_plot.shape[0] + 2))

    target_yaxis_domain = (1 - target_row_fraction, 1)

    data_yaxis_domain = (0, 1 - target_row_fraction * 2)

    data_row_fraction = (
        data_yaxis_domain[1] - data_yaxis_domain[0]
    ) / data_to_plot.shape[0]

    layout = dict(
        width=layout_width,
        height=row_height * max(8, (data_to_plot.shape[0] + 2) ** 0.8),
        margin=dict(l=layout_side_margin, r=layout_side_margin),
        xaxis=dict(anchor="y", tickfont=dict(size=annotation_font_size)),
        yaxis=dict(
            domain=data_yaxis_domain, dtick=1, tickfont=dict(size=annotation_font_size)
        ),
        yaxis2=dict(
            domain=target_yaxis_domain, tickfont=dict(size=annotation_font_size)
        ),
        title=title,
        annotations=[],
    )

    data = [
        dict(
            yaxis="y2",
            type="heatmap",
            z=target.to_frame().T.values,
            x=target.index,
            y=(target.name,),
            text=(target.index,),
            zmin=target_plot_min,
            zmax=target_plot_max,
            colorscale=target_colorscale,
            showscale=False,
        ),
        dict(
            yaxis="y",
            type="heatmap",
            z=data_to_plot.values[::-1],
            x=data_to_plot.columns,
            y=data_to_plot.index[::-1],
            zmin=data_plot_min,
            zmax=data_plot_max,
            colorscale=data_colorscale,
            showscale=False,
        ),
    ]

    layout_annotation_template = dict(
        xref="paper",
        yref="paper",
        xanchor="left",
        yanchor="middle",
        font=dict(size=annotation_font_size),
        width=64,
        showarrow=False,
    )

    for annotation_index, (annotation, strs) in enumerate(annotations.items()):

        x = 1.0016 + annotation_index / 10

        layout["annotations"].append(
            dict(
                x=x,
                y=target_yaxis_domain[1] - (target_row_fraction / 2),
                text="<b>{}</b>".format(annotation),
                **layout_annotation_template,
            )
        )

        y = data_yaxis_domain[1] - (data_row_fraction / 2)

        for str_ in strs:

            layout["annotations"].append(
                dict(
                    x=x,
                    y=y,
                    text="<b>{}</b>".format(str_),
                    **layout_annotation_template,
                )
            )

            y -= data_row_fraction

    if file_path_prefix is None:

        html_file_path = None

    else:

        html_file_path = "{}.html".format(file_path_prefix)

    if plotly_html_file_path_prefix is None:

        plotly_html_file_path = None

    else:

        plotly_html_file_path = "{}.html".format(plotly_html_file_path_prefix)

    plot_and_save(
        dict(layout=layout, data=data),
        html_file_path=html_file_path,
        plotly_html_file_path=plotly_html_file_path,
    )

    return score_moe_p_value_fdr
