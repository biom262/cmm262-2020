from numpy import asarray, nonzero, sort, unique
from pandas import DataFrame

from .check_nd_array_for_bad import check_nd_array_for_bad
from .cluster_2d_array_slices import cluster_2d_array_slices
from .COLOR_CATEGORICAL import COLOR_CATEGORICAL
from .make_colorscale import make_colorscale
from .normalize_nd_array import normalize_nd_array
from .plot_and_save import plot_and_save


def plot_heat_map(
    z,
    x=None,
    y=None,
    normalization_axis=None,
    normalization_method=None,
    column_annotation=None,
    column_annotation_str=None,
    column_annotation_colors=None,
    column_annotation_kwargs=None,
    row_annotation=None,
    row_annotation_str=None,
    row_annotation_colors=None,
    row_annotation_kwargs=None,
    sort_axis=None,
    cluster_axis=None,
    cluster_distance_function="euclidean",
    cluster_linkage_method="ward",
    colorscale=None,
    colormap="bwr",
    zmin=None,
    zmax=None,
    showscale=None,
    colorbar_x=None,
    layout_width=800,
    layout_height=800,
    heat_map_axis_domain=(0, 0.9),
    annotation_axis_domain=(0.92, 1),
    title=None,
    xaxis_title=None,
    yaxis_title=None,
    show_x_tick=True,
    show_y_tick=True,
    html_file_path=None,
    plotly_html_file_path=None,
):

    heat_map_axis_template = dict(
        domain=heat_map_axis_domain, showgrid=False, zeroline=False, automargin=True
    )

    annotation_axis_template = dict(
        showgrid=False, zeroline=False, ticks="", showticklabels=False
    )

    if xaxis_title is not None:

        xaxis_title = "{} ({})".format(xaxis_title, z.shape[1])

    if yaxis_title is not None:

        yaxis_title = "{} ({})".format(yaxis_title, z.shape[0])

    if show_x_tick is False:

        x_ticks = ""

    else:

        x_ticks = None

    if show_y_tick is False:

        y_ticks = ""

    else:

        y_ticks = None

    layout = dict(
        width=layout_width,
        height=layout_height,
        title=title,
        xaxis=dict(
            title=xaxis_title,
            ticks=x_ticks,
            showticklabels=show_x_tick,
            **heat_map_axis_template,
        ),
        xaxis2=dict(domain=annotation_axis_domain, **annotation_axis_template),
        yaxis=dict(
            title=yaxis_title,
            ticks=y_ticks,
            showticklabels=show_y_tick,
            **heat_map_axis_template,
        ),
        yaxis2=dict(domain=annotation_axis_domain, **annotation_axis_template),
    )

    if isinstance(z, DataFrame):

        x = z.columns

        y = z.index

        z = z.values

    if x is not None:

        x = asarray(x)

    if y is not None:

        y = asarray(y)

    if normalization_method:

        z = normalize_nd_array(
            z, normalization_axis, normalization_method, raise_for_bad=False
        )

    column_indices = None

    row_indices = None

    if column_annotation is not None or row_annotation is not None:

        if column_annotation is not None:

            column_indices = asarray(column_annotation).argsort()

            column_annotation = column_annotation[column_indices]

        if row_annotation is not None:

            row_indices = asarray(row_annotation).argsort()

            row_annotation = row_annotation[row_indices]

            row_annotation = row_annotation[::-1]

    elif sort_axis in (0, 1):

        z = sort(z, axis=sort_axis)

        if sort_axis == 0:

            y = None

        elif sort_axis == 1:

            x = None

    elif cluster_axis is not None:

        if not check_nd_array_for_bad(z, raise_for_bad=False).any():

            if cluster_axis == "01" or cluster_axis == 0:

                row_indices = cluster_2d_array_slices(
                    z,
                    0,
                    distance_function=cluster_distance_function,
                    linkage_method=cluster_linkage_method,
                )

            if cluster_axis == "01" or cluster_axis == 1:

                column_indices = cluster_2d_array_slices(
                    z,
                    1,
                    distance_function=cluster_distance_function,
                    linkage_method=cluster_linkage_method,
                )

    if column_indices is not None:

        z = z[:, column_indices]

        if x is not None:

            x = x[column_indices]

    if row_indices is not None:

        z = z[row_indices]

        if y is not None:

            y = y[row_indices]

    z = z[::-1]

    if y is not None:

        y = y[::-1]

    if colorscale == "COLOR_CATEGORICAL":

        colorscale = make_colorscale(
            colors=COLOR_CATEGORICAL[: unique(z).size], plot=False
        )

    elif colorscale is None and colormap is not None:

        colorscale = make_colorscale(colormap=colormap, plot=False)

    colorbar_template = dict(len=0.64, thickness=layout_width / 64)

    if column_annotation is not None or row_annotation is not None:

        colorbar_template["y"] = (heat_map_axis_domain[1] - heat_map_axis_domain[0]) / 2

    data = [
        dict(
            type="heatmap",
            z=z,
            x=x,
            y=y,
            colorscale=colorscale,
            zmin=zmin,
            zmax=zmax,
            showscale=showscale,
            colorbar=dict(x=colorbar_x, **colorbar_template),
        )
    ]

    if column_annotation is not None or row_annotation is not None:

        layout["annotations"] = []

        annotation_kwargs = dict(showarrow=False, borderpad=0)

        if column_annotation is not None:

            if column_annotation_colors is None:

                column_annotation_colors = COLOR_CATEGORICAL[
                    : len(set(column_annotation))
                ]

            data.append(
                dict(
                    yaxis="y2",
                    type="heatmap",
                    z=tuple((i,) for i in column_annotation),
                    transpose=True,
                    colorscale=make_colorscale(
                        colors=column_annotation_colors, plot=False
                    ),
                    showscale=False,
                    hoverinfo="x+z",
                )
            )

            if column_annotation_str is not None:

                if column_annotation_kwargs is None:

                    column_annotation_kwargs = dict(textangle=-90)

                for a in unique(column_annotation):

                    indices = nonzero(column_annotation == a)[0]

                    index_0 = indices[0]

                    layout["annotations"].append(
                        dict(
                            yref="y2",
                            x=index_0 + (indices[-1] - index_0) / 2,
                            y=0,
                            text="<b>{}</b>".format(column_annotation_str[a]),
                            **annotation_kwargs,
                            **column_annotation_kwargs,
                        )
                    )

        if row_annotation is not None:

            if row_annotation_colors is None:

                row_annotation_colors = COLOR_CATEGORICAL[: len(set(row_annotation))]

            data.append(
                dict(
                    xaxis="x2",
                    type="heatmap",
                    z=tuple((i,) for i in row_annotation),
                    colorscale=make_colorscale(
                        colors=row_annotation_colors, plot=False
                    ),
                    showscale=False,
                    hoverinfo="y+z",
                )
            )

            if row_annotation_str is not None:

                if row_annotation_kwargs is None:

                    row_annotation_kwargs = dict()

                for a in unique(row_annotation):

                    indices = nonzero(row_annotation == a)[0]

                    index_0 = indices[0]

                    layout["annotations"].append(
                        dict(
                            xref="x2",
                            x=0,
                            y=index_0 + (indices[-1] - index_0) / 2,
                            text="<b>{}</b>".format(row_annotation_str[a]),
                            **annotation_kwargs,
                            **row_annotation_kwargs,
                        )
                    )

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
