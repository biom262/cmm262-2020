from numpy import apply_along_axis, rot90

from .plot_heat_map import plot_heat_map


def compute_posterior_probability(probability, plot=True, names=None):

    n_dimension = probability.ndim

    p_tv__ntvs = apply_along_axis(
        lambda _1d_array: _1d_array / _1d_array.sum(), n_dimension - 1, probability
    )

    if plot and n_dimension == 2:

        if names is None:

            names = tuple("variables[{}]".format(i) for i in range(n_dimension))

        plot_heat_map(
            rot90(p_tv__ntvs),
            title="P({} | {})".format(names[1], names[0]),
            xaxis_title=names[0],
            yaxis_title=names[1],
        )

    return p_tv__ntvs
