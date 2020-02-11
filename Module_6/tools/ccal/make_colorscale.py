from .get_colormap_colors import get_colormap_colors
from .make_categorical_colors import make_categorical_colors
from .make_colorscale_from_colors import make_colorscale_from_colors
from .plot_and_save import plot_and_save


def make_colorscale(
    colorscale=None,
    colors=None,
    colormap=None,
    n_category=None,
    plot=True,
    layout_width=None,
    layout_height=None,
    title=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    if colorscale is not None:

        colorscale = colorscale

    elif colors is not None:

        colorscale = make_colorscale_from_colors(colors)

    elif colormap is not None:

        colorscale = make_colorscale_from_colors(get_colormap_colors(colormap))

    elif n_category is not None:

        colorscale = make_colorscale_from_colors(make_categorical_colors(n_category))

    if plot:

        x = tuple(range(len(colorscale)))

        colors = tuple(t[1] for t in colorscale)

        plot_and_save(
            dict(
                layout=dict(
                    width=layout_width,
                    height=layout_height,
                    title=title,
                    xaxis=dict(tickmode="array", tickvals=x, ticktext=colors),
                    yaxis=dict(ticks="", showticklabels=False),
                ),
                data=[
                    dict(
                        type="heatmap",
                        z=(x,),
                        colorscale=colorscale,
                        showscale=False,
                        hoverinfo="x+text",
                    )
                ],
            ),
            html_file_path,
            plotly_html_file_path,
        )

    return colorscale
