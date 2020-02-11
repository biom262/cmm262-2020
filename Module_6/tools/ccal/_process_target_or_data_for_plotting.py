from numpy import nanmax, nanmin, unique
from pandas import DataFrame, Series

from .COLOR_CATEGORICAL import COLOR_CATEGORICAL
from .COLOR_WHITE_BLACK import COLOR_WHITE_BLACK
from .make_colorscale import make_colorscale
from .normalize_nd_array import normalize_nd_array


def _process_target_or_data_for_plotting(target_or_data, type, plot_std):

    if type == "continuous":

        if isinstance(target_or_data, Series):

            target_or_data = Series(
                normalize_nd_array(
                    target_or_data.values, None, "-0-", raise_for_bad=False
                ),
                name=target_or_data.name,
                index=target_or_data.index,
            )

        elif isinstance(target_or_data, DataFrame):

            target_or_data = DataFrame(
                normalize_nd_array(
                    target_or_data.values, 1, "-0-", raise_for_bad=False
                ),
                index=target_or_data.index,
                columns=target_or_data.columns,
            )

        target_or_data_nanmin = nanmin(target_or_data.values)

        target_or_data_nanmax = nanmax(target_or_data.values)

        if plot_std is None:

            plot_min = target_or_data_nanmin

            plot_max = target_or_data_nanmax

        else:

            plot_min = -plot_std

            plot_max = plot_std

        colorscale = make_colorscale(colormap="bwr", plot=False)

    else:

        plot_min = None

        plot_max = None

        if type == "categorical":

            n_color = unique(target_or_data).size

            colorscale = make_colorscale(colors=COLOR_CATEGORICAL[:n_color], plot=False)

        elif type == "binary":

            colorscale = make_colorscale(colors=COLOR_WHITE_BLACK, plot=False)

    return target_or_data, plot_min, plot_max, colorscale
