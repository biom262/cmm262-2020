from numpy import absolute, argmax, linspace, rot90

from ._get_target_grid_indices import _get_target_grid_indices
from ._plot_2d import _plot_2d
from .compute_joint_probability import compute_joint_probability
from .compute_posterior_probability import compute_posterior_probability
from .plot_points import plot_points


def infer(
    variables,
    variable_types=None,
    bandwidths="normal_reference",
    grid_size=64,
    target="max",
    plot=True,
    names=None,
):

    print("\nInfering ...")

    n_dimension = len(variables)

    if variable_types is None:

        variable_types = "c" * n_dimension

    print("\tComputing P(variables)...")

    if plot:

        if names is None:

            names = tuple("variables[{}]".format(i) for i in range(n_dimension))

    p_vs = compute_joint_probability(
        variables,
        variable_types=variable_types,
        bandwidths=bandwidths,
        grid_size=grid_size,
        plot_kernel_density=False,
        plot_probability=plot,
        names=names,
    )

    print("\tComputing P(target variable | non-target variables) ...")

    p_tv__ntvs = compute_posterior_probability(p_vs, plot=plot, names=names)

    print("\tGetting target grid coordinates ...")

    if target is "max":

        t_grid_coordinates = _get_target_grid_indices(p_tv__ntvs, argmax)

    else:

        t_grid = linspace(variables[-1].min(), variables[-1].max(), grid_size)

        t_i = absolute(t_grid - target).argmin()

        t_grid_coordinates = _get_target_grid_indices(p_tv__ntvs, lambda _: t_i)

    print("\tComputing P(target variable = target | non-target variables) ...")

    p_tvt__ntvs = p_tv__ntvs[t_grid_coordinates].reshape(
        (grid_size,) * (n_dimension - 1)
    )

    if plot:

        if n_dimension == 2:

            title = "P({} = {} | {})".format(names[-1], target, names[0])

            plot_points(
                (tuple(range(grid_size)),),
                (p_tvt__ntvs,),
                names=(title,),
                title=title,
                xaxis_title=names[0],
                yaxis_title="Probability",
            )

        elif n_dimension == 3:

            _plot_2d(
                rot90(p_tvt__ntvs),
                "P({} = {} | {}, {})".format(names[-1], target, names[0], names[1]),
                names[0],
                names[1],
            )

    return p_tv__ntvs, p_tvt__ntvs
