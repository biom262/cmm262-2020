from numpy import asarray, cos, insert, linspace, pi, sin

from .COLOR_CATEGORICAL import COLOR_CATEGORICAL
from .plot_and_save import plot_and_save


def plot_pie(
    values,
    labels,
    colors=None,
    textinfo=None,
    insidetextfont=None,
    outsidetextfont=None,
    hole=None,
    pie_domain_range=1,
    showlegend=None,
    annotations=None,
    annotation_font_colors=None,
    annotation_background_colors=None,
    annotation_border_colors=None,
    annotation_font_size=None,
    annotation_width=None,
    annotation_border_width=None,
    hole_text=None,
    hole_text_font=None,
    layout_width=None,
    layout_height=None,
    layout_margin=None,
    title=None,
    html_file_path=None,
    plotly_html_file_path=None,
):

    values = asarray(values)

    labels = asarray(labels)

    if colors is not None:

        colors = asarray(colors)

    if annotations is not None:

        annotations = asarray(annotations)

    if annotation_font_colors is not None:

        annotation_font_colors = asarray(annotation_font_colors)

    if annotation_background_colors is not None:

        annotation_background_colors = asarray(annotation_background_colors)

    if annotation_border_colors is not None:

        annotation_border_colors = asarray(annotation_border_colors)

    non_0_value = values != 0

    values = values[non_0_value]

    labels = labels[non_0_value]

    if colors is not None:

        colors = colors[non_0_value]

    if annotations is not None:

        annotations = annotations[non_0_value]

    if annotation_font_colors is not None:

        annotation_font_colors = annotation_font_colors[non_0_value]

    if annotation_background_colors is not None:

        annotation_background_colors = annotation_background_colors[non_0_value]

    if annotation_border_colors is not None:

        annotation_border_colors = annotation_border_colors[non_0_value]

    order = values.argsort()[::-1]

    values = values[order]

    labels = labels[order]

    if colors is not None:

        colors = colors[order]

    if annotations is not None:

        annotations = annotations[order]

    if annotation_font_colors is not None:

        annotation_font_colors = annotation_font_colors[order]

    if annotation_background_colors is not None:

        annotation_background_colors = annotation_background_colors[order]

    if annotation_border_colors is not None:

        annotation_border_colors = annotation_border_colors[order]

    axis_template = dict(showgrid=False, zeroline=False, ticks="", showticklabels=False)

    layout = dict(
        width=layout_width,
        height=layout_height,
        margin=dict(l=layout_margin, r=layout_margin, b=layout_margin, t=layout_margin),
        title=title,
        xaxis=dict(**axis_template),
        yaxis=dict(**axis_template),
    )

    if colors is None:

        colors = COLOR_CATEGORICAL

    if insidetextfont is None:

        insidetextfont = dict(color="#ebf6f7")

    if outsidetextfont is None:

        outsidetextfont = dict(color="#000000")

    data = [
        dict(
            type="pie",
            values=values,
            labels=labels,
            opacity=0.8,
            marker=dict(colors=colors, line=dict(width=1.6, color="#ffffff")),
            textinfo=textinfo,
            insidetextfont=insidetextfont,
            outsidetextfont=outsidetextfont,
            hole=hole,
            sort=False,
            direction="clockwise",
            domain=dict(
                x=(1 - pie_domain_range, pie_domain_range),
                y=(1 - pie_domain_range, pie_domain_range),
            ),
            showlegend=showlegend,
        )
    ]

    annotation_template = dict(xref="x", yref="y", showarrow=False)

    layout_annotations = []

    if hole is not None and hole_text is not None:

        layout_annotations.append(
            dict(
                x=0,
                y=0,
                text="<b>{}</b>".format(hole_text),
                font=hole_text_font,
                **annotation_template,
            )
        )

    if annotations is not None:

        radians = insert(-pi * 2 * (values / values.sum()).cumsum(), 0, 0)

        for i in range(radians.size - 1):

            radian_0 = radians[i]

            radian_1 = radians[i + 1]

            label_annotations = asarray(annotations[i])

            for j, (radian, annotation) in enumerate(
                zip(
                    linspace(radian_0, radian_1, len(label_annotations) + 2)[1:-1],
                    label_annotations,
                )
            ):

                annotation_text_angle = -radian / pi * 180

                if annotation_text_angle < 180:

                    annotation_text_angle -= 90

                else:

                    annotation_text_angle += 90

                if annotation_font_colors is None:

                    annotation_font_color = colors[i]

                else:

                    annotation_font_color = annotation_font_colors[i][j]

                if annotation_background_colors is None:

                    annotation_background_color = None

                else:

                    annotation_background_color = annotation_background_colors[i][j]

                if annotation_border_colors is None:

                    annotation_border_color = None

                else:

                    annotation_border_color = annotation_border_colors[i][j]

                layout_annotations.append(
                    dict(
                        x=cos(radian + pi / 2),
                        y=sin(radian + pi / 2),
                        text="<b>{}</b>".format(annotation),
                        textangle=annotation_text_angle,
                        font=dict(
                            size=annotation_font_size, color=annotation_font_color
                        ),
                        bgcolor=annotation_background_color,
                        bordercolor=annotation_border_color,
                        width=annotation_width,
                        borderwidth=annotation_border_width,
                        **annotation_template,
                    )
                )

    layout.update(annotations=layout_annotations)

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
