from .make_colorscale import make_colorscale
from .plot_and_save import plot_and_save


def _plot_2d(_2d_array, title, xaxis_title, yaxis_title, layout_size=None):

    layout = dict(
        width=layout_size,
        height=layout_size,
        title=title,
        xaxis=dict(title=xaxis_title),
        yaxis=dict(title=yaxis_title),
    )

    if layout_size is None:

        colorbar_thickness = None

    else:

        colorbar_thickness = layout_size / 80

    data = [
        dict(
            type="heatmap",
            z=_2d_array[::-1],
            colorscale=make_colorscale(colormap="bwr", plot=False),
            colorbar=dict(len=0.8, thickness=colorbar_thickness),
        )
    ]

    plot_and_save(dict(layout=layout, data=data), None, None)
