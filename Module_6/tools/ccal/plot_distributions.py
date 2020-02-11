from pandas import Series

from .COLOR_CATEGORICAL import COLOR_CATEGORICAL
from .plot_and_save import plot_and_save


def plot_distributions(
    xs,
    names=None,
    texts=None,
    colors=None,
    histnorm="",
    plot_rug=True,
    layout_width=None,
    layout_height=None,
    title=None,
    xaxis_title=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    if plot_rug:

        yaxis_max = 0.16

        yaxis2_min = yaxis_max + 0.08

    else:

        yaxis_max = 0

        yaxis2_min = 0

    layout = dict(
        width=layout_width,
        height=layout_height,
        title=title,
        xaxis=dict(anchor="y", title=xaxis_title),
        yaxis=dict(
            domain=(0, yaxis_max), dtick=1, zeroline=False, showticklabels=False
        ),
        yaxis2=dict(domain=(yaxis2_min, 1), title=histnorm.title()),
        barmode="overlay",
    )

    data = []

    for i, x in enumerate(xs):

        if names is None:

            name = None

        else:

            name = names[i]

        if colors is None:

            color = COLOR_CATEGORICAL[i]

        else:

            color = colors[i]

        data.append(
            dict(
                yaxis="y2",
                type="histogram",
                name=name,
                legendgroup=i,
                x=x,
                marker=dict(color=color),
                histnorm=histnorm,
                opacity=0.8,
                hoverinfo="x+y",
            )
        )

        if plot_rug:

            if texts is None:

                if isinstance(x, Series):

                    text = x.index

                else:

                    text = None

            else:

                text = texts[i]

            data.append(
                dict(
                    type="scatter",
                    legendgroup=i,
                    showlegend=False,
                    x=x,
                    y=(i,) * len(x),
                    text=text,
                    mode="markers",
                    marker=dict(symbol="line-ns-open", color=color),
                    hoverinfo="x+text",
                )
            )

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
