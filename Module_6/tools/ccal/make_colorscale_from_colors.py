def make_colorscale_from_colors(colors):

    if len(colors) == 1:

        colors *= 2

    return tuple((i / (len(colors) - 1), color) for i, color in enumerate(colors))
