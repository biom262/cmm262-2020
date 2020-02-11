from .plot_and_save import plot_and_save


def plot_color_text(
    colors,
    texts,
    orientation="vertical",
    marker_size=None,
    textfont_size=None,
    layout_width=None,
    layout_height=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    axis = dict(showgrid=False, zeroline=False, ticks="", showticklabels=False)

    if orientation == "horizontal":

        x = tuple(range(len(colors)))

        y = (0,) * len(colors)

        textposition = "bottom center"

    elif orientation == "vertical":

        x = (0,) * len(colors)

        y = tuple(range(len(colors)))

        textposition = "middle right"

    plot_and_save(
        dict(
            layout=dict(
                width=layout_width, height=layout_height, xaxis=axis, yaxis=axis
            ),
            data=[
                dict(
                    type="scatter",
                    mode="markers+text",
                    x=x,
                    y=y,
                    text=texts,
                    marker=dict(size=marker_size, color=colors),
                    textposition=textposition,
                    textfont=dict(size=textfont_size),
                )
            ],
        ),
        html_file_path,
        plotly_html_file_path,
    )
