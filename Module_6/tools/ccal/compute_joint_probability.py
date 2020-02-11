from numpy import rot90

from .estimate_kernel_density import estimate_kernel_density
from .plot_heat_map import plot_heat_map


def compute_joint_probability(
    variables,
    variable_types=None,
    bandwidths="normal_reference",
    grid_size=64,
    plot_kernel_density=True,
    plot_probability=True,
    names=None,
):

    n_dimension = len(variables)

    if variable_types is None:

        variable_types = "c" * n_dimension

    kernel_density = estimate_kernel_density(
        variables,
        variable_types,
        bandwidths=bandwidths,
        grid_sizes=(grid_size,) * n_dimension,
    )

    probability = kernel_density / kernel_density.sum()

    if n_dimension == 2:

        if names is None:

            names = tuple("variables[{}]".format(i) for i in range(n_dimension))

        if plot_kernel_density:

            plot_heat_map(
                rot90(kernel_density),
                title="KDE({}, {})".format(names[0], names[1]),
                xaxis_title=names[0],
                yaxis_title=names[1],
            )

        if plot_probability:

            plot_heat_map(
                rot90(probability),
                title="P({}, {})".format(names[0], names[1]),
                xaxis_title=names[0],
                yaxis_title=names[1],
            )

    return probability
