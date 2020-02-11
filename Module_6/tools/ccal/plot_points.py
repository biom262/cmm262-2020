from .COLOR_CATEGORICAL import COLOR_CATEGORICAL
from .plot_and_save import plot_and_save


def plot_points(
    xs,
    ys,
    names=None,
    modes=None,
    texts=None,
    markers=None,
    textpositions=None,
    layout_width=None,
    layout_height=None,
    title=None,
    xaxis_title=None,
    yaxis_title=None,
    legend_orientation=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    layout = dict(
        width=layout_width,
        height=layout_height,
        title=title,
        xaxis=dict(title=xaxis_title),
        yaxis=dict(title=yaxis_title),
        legend=dict(orientation=legend_orientation),
        hovermode="closest",
    )

    data = []

    for i, (x, y) in enumerate(zip(xs, ys)):

        if names is None:

            name = None

        else:

            name = names[i]

        if modes is None:

            mode = "markers"

        else:

            mode = modes[i]

        if texts is None:

            text = None

        else:

            text = texts[i]

        if markers is None:

            marker = dict(color=COLOR_CATEGORICAL[i])

        else:

            marker = markers[i]

        if textpositions is None:

            textposition = None

        else:

            textposition = textpositions[i]

        data.append(
            dict(
                type="scatter",
                name=name,
                x=x,
                y=y,
                mode=mode,
                text=text,
                textfont = dict(
                    color = "#9017e6",
                    size = 5
                    ),
                marker=marker,
                textposition=textposition,
            )
        )

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
