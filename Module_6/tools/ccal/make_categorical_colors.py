from matplotlib.colors import to_hex
from seaborn import husl_palette


def make_categorical_colors(n_category):

    return tuple(to_hex(rgb) for rgb in husl_palette(n_colors=n_category))
