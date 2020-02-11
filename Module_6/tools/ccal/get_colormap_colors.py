from matplotlib.cm import get_cmap
from matplotlib.colors import to_hex


def get_colormap_colors(colormap):

    if isinstance(colormap, str):

        colormap = get_cmap(colormap)

    return tuple(to_hex(colormap(i / (colormap.N - 1))) for i in range(colormap.N))
