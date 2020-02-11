from numpy import linspace, meshgrid

from .make_colorscale import make_colorscale
from .normalize_nd_array import normalize_nd_array
from .plot_and_save import plot_and_save


def plot_bubble_map(
    df_size,
    _2d_array_color=None,
    colormap_name="bwr",
    marker_size_max=32,
    title=None,
    xaxis_title=None,
    yaxis_title=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    layout_width = max(640, marker_size_max * 2 * df_size.shape[1])

    layout_height = max(640, marker_size_max * 2 * df_size.shape[0])

    axis_template = dict(zeroline=False, automargin=True)

    layout = dict(
        width=layout_width,
        height=layout_height,
        title=title,
        xaxis=dict(
            tickvals=tuple(range(df_size.shape[1])),
            ticktext=df_size.columns,
            title="{} ({})".format(xaxis_title, df_size.shape[1]),
            **axis_template,
        ),
        yaxis=dict(
            tickvals=tuple(range(df_size.shape[0])),
            ticktext=df_size.index[::-1],
            title="{} ({})".format(yaxis_title, df_size.shape[0]),
            **axis_template,
        ),
    )

    x, y = meshgrid(
        linspace(0, df_size.shape[1] - 1, df_size.shape[1]),
        linspace(0, df_size.shape[0] - 1, df_size.shape[0]),
    )

    if _2d_array_color is None:

        _2d_array_color = df_size.values

    data = [
        dict(
            type="scatter",
            x=x.ravel(),
            y=y.ravel()[::-1],
            text=df_size.values.ravel(),
            mode="markers",
            marker=dict(
                size=normalize_nd_array(df_size.values, None, "0-1").ravel()
                * marker_size_max,
                color=_2d_array_color.ravel(),
                colorscale=make_colorscale(colormap=colormap_name, plot=False),
                showscale=True,
                colorbar=dict(len=0.64, thickness=marker_size_max / 3),
                line=dict(color="#000000"),
            ),
        )
    ]

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
