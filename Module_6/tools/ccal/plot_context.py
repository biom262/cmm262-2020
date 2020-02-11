from numpy import absolute, nanmax
from pandas import Series

from .compute_context import compute_context
from .plot_and_save import plot_and_save


def plot_context(
    _1d_array_or_series,
    text=None,
    n_data=None,
    location=None,
    scale=None,
    degree_of_freedom=None,
    shape=None,
    fit_initial_location=None,
    fit_initial_scale=None,
    n_grid=1e3,
    degree_of_freedom_for_tail_reduction=1e8,
    multiply_distance_from_reference_argmax=False,
    global_location=None,
    global_scale=None,
    global_degree_of_freedom=None,
    global_shape=None,
    y_max_is_pdf_max=False,
    n_bin=None,
    plot_rug=True,
    layout_width=None,
    layout_height=None,
    title=None,
    xaxis_title=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    if isinstance(_1d_array_or_series, Series):

        if title is None:

            title = _1d_array_or_series.name


        if xaxis_title is None:

            xaxis_title = "Value"

        if text is None:

            text = _1d_array_or_series.index

        _1d_array = _1d_array_or_series.values

    else:

        _1d_array = _1d_array_or_series

    context_dict = compute_context(
        _1d_array,
        n_data=n_data,
        location=location,
        scale=scale,
        degree_of_freedom=degree_of_freedom,
        shape=shape,
        fit_initial_location=fit_initial_location,
        fit_initial_scale=fit_initial_scale,
        n_grid=n_grid,
        degree_of_freedom_for_tail_reduction=degree_of_freedom_for_tail_reduction,
        multiply_distance_from_reference_argmax=multiply_distance_from_reference_argmax,
        global_location=global_location,
        global_scale=global_scale,
        global_degree_of_freedom=global_degree_of_freedom,
        global_shape=global_shape,
    )

    pdf_max = context_dict["pdf"].max()

    context_indices = context_dict["context_indices"]

    absolute_context_indices = absolute(context_indices)

    absolute_context_indices_max = nanmax(absolute_context_indices)

    if y_max_is_pdf_max:

        y_max = pdf_max

        if y_max < absolute_context_indices_max:

            absolute_context_indices = (
                absolute_context_indices / absolute_context_indices_max * y_max
            )

    else:

        y_max = max(pdf_max, absolute_context_indices_max)

    if plot_rug:

        yaxis_max = 0.04

        yaxis2_min = yaxis_max + 0.04

    else:

        yaxis_max = 0

        yaxis2_min = 0

    layout = dict(
        width=layout_width,
        height=layout_height,
        title=title,
        xaxis=dict(anchor="y", title=xaxis_title),
        yaxis=dict(domain=(0, yaxis_max), # domain=(0, yaxis_max),
            dtick=1, zeroline=False, showticklabels=False
        ),
        yaxis2=dict(domain=(yaxis2_min, 1)),
        legend=dict(orientation="v", xanchor="center", x=1.035, y=0.9,
                        bgcolor="#FFFFFF", font=dict(family="Arial", size=12))
    ) 

    annotations = []

    for i, (template, fit_parameter) in enumerate(
        zip(
            (
                "N = {:.0f}",
                "Location = {:.2f}",
                "Scale = {:.2f}",
                "DF = {:.2f}",
                "Shape = {:.2f}",
            ),
            context_dict["fit"],
        )
    ):

        annotations.append(
            dict(
                xref="paper",
                yref="paper",
                x=(i + 1) / (5 + 1),
                y=1.064,
                xanchor="center",
                text=template.format(fit_parameter),
                showarrow=False,
            )
        )

    layout.update(annotations=annotations)

    data = []

    data.append(
        dict(
            yaxis="y2",
            type="histogram",
            name="Histogram",
            legendgroup="Data",
            x=_1d_array,
            marker=dict(color="#20d9ba", line=dict(width = 0.5)),
            histnorm="probability density",
            hoverinfo="x+y",
        )
    )

    if n_bin is not None:

        _1d_array_min = _1d_array.min()

        _1d_array_max = _1d_array.max()

        data[-1]["xbins"] = dict(
            start=_1d_array_min,
            end=_1d_array_max,
            size=(_1d_array_max - _1d_array_min) / n_bin,
        )

    if plot_rug:

        data.append(
            dict(
                type="scatter",
                legendgroup="Data",
                name="Data",
                showlegend=True,
                x=_1d_array,
                y=(0,) * _1d_array.size, # (0,) * _1d_array.size,
                text=text,
                mode="markers",
                marker=dict(symbol="line-ns-open", color="#000000"), # "#20d9ba"),
                hoverinfo="x+text",
            )
        )

    grid = context_dict["grid"]

    line_width = 3.2

    pdf = context_dict["pdf"]

    data.append(
        dict(
            yaxis="y2",
            type="scatter",
            name="PDF",
            x=grid,
            y=pdf,
            line=dict(width=line_width, color="#9017e6"), # "#24e7c0"),
        )
    )

    shape_pdf_reference = context_dict["shape_pdf_reference"]

    shape_pdf_reference[pdf <= shape_pdf_reference] = None

    data.append(
        dict(
            yaxis="y2",
            type="scatter",
            name="Null PDF",
            x=grid,
            y=shape_pdf_reference,
            line=dict(width=line_width, color="#FF6600"),
        )
    )

    location_pdf_reference = context_dict["location_pdf_reference"]

    if location_pdf_reference is not None:

        location_pdf_reference[pdf <= location_pdf_reference] = None

        data.append(
            dict(
                yaxis="y2",
                type="scatter",
                name="Location Reference",
                x=grid,
                y=location_pdf_reference,
                line=dict(width=line_width, color="#4e40d8"),
            )
        )

    is_negative = context_dict["context_indices"] < 0

    is_positive = 0 < context_dict["context_indices"]

    for name, indices, color in (
        ("- Context", is_negative, "#0088ff"),
        ("+ Context", is_positive, "#ff1968"),
    ):

        data.append(
            dict(
                yaxis="y2",
                type="scatter",
                name=name,
                x=grid[indices],
                y=absolute_context_indices[indices],
                line=dict(width=line_width, color=color),
                fill="tozeroy",
            )
        )

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
