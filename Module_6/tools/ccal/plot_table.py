from .plot_and_save import plot_and_save


def plot_table(
    df,
    align="center",
    header_color="#ebf6f7",
    cells_color="#f8f8f8",
    columnwidth=None,
    width_per_column=64,
    height_per_row=42,
    title=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    layout = dict(
        width=width_per_column * max(8, df.shape[1]),
        height=height_per_row * max(8, df.shape[0]),
        title=title,
    )

    align = (align,) * df.columns.size

    if df.index.name is None:

        index_name = ""

    else:

        index_name = df.index.name

    header_values = tuple(
        "<b>{}</b>".format(str_) for str_ in (index_name,) + tuple(df.columns)
    )

    cells_values = (tuple("<b>{}</b>".format(str_) for str_ in df.index),) + tuple(
        df[column] for column in df.columns
    )

    data = [
        dict(
            type="table",
            header=dict(
                values=header_values, align=align, fill=dict(color=header_color)
            ),
            cells=dict(
                values=cells_values,
                align=align,
                fill=dict(color=(header_color, cells_color)),
            ),
            columnwidth=columnwidth,
        )
    ]

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
