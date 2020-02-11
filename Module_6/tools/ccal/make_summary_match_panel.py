from ._make_annotations import _make_annotations
from ._process_target_or_data_for_plotting import _process_target_or_data_for_plotting
from .ALMOST_ZERO import ALMOST_ZERO
from .plot_and_save import plot_and_save


def make_summary_match_panel(
    target,
    data_dicts,
    score_moe_p_value_fdr_dicts,
    plot_only_columns_shared_by_target_and_all_data=False,
    target_ascending=True,
    target_type="continuous",
    score_ascending=False,
    plot_std=None,
    title=None,
    layout_width=880,
    row_height=64,
    layout_side_margin=196,
    annotation_font_size=10,
    xaxis_kwargs=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    if plot_only_columns_shared_by_target_and_all_data:

        for data_dict in data_dicts.values():

            target = target.loc[target.index & data_dict["df"].columns]

    if target_ascending is not None:

        target.sort_values(ascending=target_ascending, inplace=True)

    target, target_plot_min, target_plot_max, target_colorscale = _process_target_or_data_for_plotting(
        target, target_type, plot_std
    )

    n_row = 1 + len(data_dicts)

    for data_dict in data_dicts.values():

        n_row += data_dict["df"].shape[0]

    layout = dict(
        width=layout_width,
        height=row_height / 2 * max(10, n_row),
        margin=dict(l=layout_side_margin, r=layout_side_margin),
        title=title,
        xaxis=dict(anchor="y", **xaxis_kwargs),
        annotations=[],
    )

    row_fraction = 1 / n_row

    yaxis_name = "yaxis{}".format(len(data_dicts) + 1)

    domain_end = 1

    domain_start = domain_end - row_fraction

    if abs(domain_start) <= ALMOST_ZERO:

        domain_start = 0

    layout[yaxis_name] = dict(
        domain=(domain_start, domain_end), tickfont=dict(size=annotation_font_size)
    )

    data = [
        dict(
            yaxis=yaxis_name.replace("axis", ""),
            type="heatmap",
            z=target.to_frame().T.values,
            x=target.index,
            y=(target.name,),
            text=(target.index,),
            zmin=target_plot_min,
            zmax=target_plot_max,
            colorscale=target_colorscale,
            showscale=False,
        )
    ]

    for data_name_index, (data_name, data_dict) in enumerate(data_dicts.items()):

        print("Making match panel for {} ...".format(data_name))

        df = data_dict["df"]

        data_to_plot = df.reindex(columns=target.index)

        score_moe_p_value_fdr_to_plot = score_moe_p_value_fdr_dicts[data_name].loc[
            data_to_plot.index
        ]

        score_moe_p_value_fdr_to_plot.sort_values(
            "Score", ascending=score_ascending, inplace=True
        )

        data_to_plot = data_to_plot.loc[score_moe_p_value_fdr_to_plot.index]

        annotations = _make_annotations(score_moe_p_value_fdr_to_plot)

        data_to_plot, data_plot_min, data_plot_max, data_colorscale = _process_target_or_data_for_plotting(
            data_to_plot, data_dict["type"], plot_std
        )

        yaxis_name = "yaxis{}".format(len(data_dicts) - data_name_index)

        domain_end = domain_start - row_fraction

        if abs(domain_end) <= ALMOST_ZERO:

            domain_end = 0

        domain_start = domain_end - data_dict["df"].shape[0] * row_fraction

        if abs(domain_start) <= ALMOST_ZERO:

            domain_start = 0

        layout[yaxis_name] = dict(
            domain=(domain_start, domain_end),
            dtick=1,
            tickfont=dict(size=annotation_font_size),
        )

        data.append(
            dict(
                yaxis=yaxis_name.replace("axis", ""),
                type="heatmap",
                z=data_to_plot.values[::-1],
                x=data_to_plot.columns,
                y=data_to_plot.index[::-1],
                zmin=data_plot_min,
                zmax=data_plot_max,
                colorscale=data_colorscale,
                showscale=False,
            )
        )

        layout_annotation_template = dict(
            xref="paper",
            yref="paper",
            yanchor="middle",
            font=dict(size=annotation_font_size),
            showarrow=False,
        )

        layout["annotations"].append(
            dict(
                xanchor="center",
                x=0.5,
                y=domain_end + (row_fraction / 2),
                text="<b>{}</b>".format(data_name),
                **layout_annotation_template,
            )
        )

        layout_annotation_template.update(dict(xanchor="left", width=64))

        for (
            annotation_index,
            (annotation_column_name, annotation_column_strs),
        ) in enumerate(annotations.items()):

            x = 1.0016 + annotation_index / 10

            if data_name_index == 0:

                layout["annotations"].append(
                    dict(
                        x=x,
                        y=1 - (row_fraction / 2),
                        text="<b>{}</b>".format(annotation_column_name),
                        **layout_annotation_template,
                    )
                )

            y = domain_end - (row_fraction / 2)

            for str_ in annotation_column_strs:

                layout["annotations"].append(
                    dict(
                        x=x,
                        y=y,
                        text="<b>{}</b>".format(str_),
                        **layout_annotation_template,
                    )
                )

                y -= row_fraction

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
