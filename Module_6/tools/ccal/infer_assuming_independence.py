from numpy import absolute, full, linspace, meshgrid, nan, product, rot90

from ._plot_2d import _plot_2d
from .estimate_kernel_density import estimate_kernel_density
from .infer import infer
from .plot_points import plot_points


def infer_assuming_independence(
    variables,
    variable_types=None,
    bandwidths="normal_reference",
    grid_size=64,
    target="max",
    plot=True,
    names=None,
):

    print("\nInfering assuming independence ...")

    n_dimension = len(variables)

    if variable_types is None:

        variable_types = "c" * n_dimension

    n_ntvs = n_dimension - 1

    if isinstance(bandwidths, str):

        target_bandwidth = bandwidths

    else:

        target_bandwidth = bandwidths[-1]

    kd_tv = estimate_kernel_density(
        (variables[-1],),
        variable_types[-1],
        bandwidths=target_bandwidth,
        grid_sizes=(grid_size,),
    )

    p_tv = kd_tv / kd_tv.sum()

    grid_tv = linspace(variables[-1].min(), variables[-1].max(), grid_size)

    if target == "max":

        t_i = p_tv.argmax()

    else:

        t_i = absolute(grid_tv - target).argmin()

    t = grid_tv[t_i]

    p_tvt = p_tv[t_i]

    if plot:

        if names is None:

            names = tuple("variables[{}]".format(i) for i in range(n_dimension))

    if plot:

        title = "P({} = {:.2f}) = {:.2f}".format(names[-1], t, p_tvt)

        plot_points(
            (grid_tv,),
            (p_tv,),
            names=(title,),
            title=title,
            xaxis_title=names[-1],
            yaxis_title="Probability",
        )

    p_tvt__1ntvs = []

    for ntv_i in range(n_ntvs):

        if isinstance(bandwidths, str):

            bandwidths_ = bandwidths

        else:

            bandwidths_ = (bandwidths[ntv_i], bandwidths[-1])

        p_tvt__1ntv = infer(
            (variables[ntv_i], variables[-1]),
            variable_types=variable_types[ntv_i] + variable_types[-1],
            bandwidths=bandwidths_,
            grid_size=grid_size,
            target=target,
            plot=False,
            names=(names[ntv_i], names[-1]),
        )[1]

        p_tvt__1ntvs.append(p_tvt__1ntv)

    p_tvt__ntvs = full((grid_size,) * n_ntvs, nan)

    ntvs_igrid_meshgrid_ravel = tuple(
        meshgrid_.astype(int).ravel()
        for meshgrid_ in meshgrid(
            *(linspace(0, grid_size - 1, grid_size),) * n_ntvs, indexing="ij"
        )
    )

    for i in range(grid_size ** n_ntvs):

        coordinate = [[ntvs_igrid_meshgrid_ravel[ntv_i][i]] for ntv_i in range(n_ntvs)]

        p_tvt__ntvs[coordinate] = product(
            [p_tvt__1ntvs[j][coordinate[j]] for j in range(n_ntvs)]
        ) / p_tvt ** (n_ntvs - 1)

    if plot and n_dimension == 3:

        _plot_2d(
            rot90(p_tvt__ntvs),
            "P({} = {} | {}, {})".format(names[2], target, names[0], names[1]),
            names[0],
            names[1],
        )

    return None, p_tvt__ntvs
