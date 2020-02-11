from .COLOR_CATEGORICAL import COLOR_CATEGORICAL
from .plot_and_save import plot_and_save


def plot_violin_or_box(
    ys,
    xs=None,
    names=None,
    colors=None,
    violin_or_box="violin",
    points="all",
    pointpos=0,
    jitter=None,
    layout_width=None,
    layout_height=None,
    title=None,
    xaxis_title=None,
    yaxis_title=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    layout = dict(
        width=layout_width,
        height=layout_height,
        title=title,
        xaxis=dict(title=xaxis_title),
        yaxis=dict(title=yaxis_title),
    )

    data = []

    for i, y in enumerate(ys):

        if xs is None:

            x = None

        else:

            x = xs[i]

        if names is None:

            name = None

        else:

            name = names[i]

        if colors is None:

            color = COLOR_CATEGORICAL[i]

        else:

            color = colors[i]

        if violin_or_box == "violin":

            arguments = dict(
                scalemode="count", meanline=dict(visible=True), points=points
            )

        elif violin_or_box == "box":

            arguments = dict(boxmean="sd", boxpoints=points)

        data.append(
            dict(
                type=violin_or_box,
                name=name,
                x=x,
                y=y,
                pointpos=pointpos,
                jitter=jitter,
                marker=dict(color=color),
                **arguments,
            )
        )

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
