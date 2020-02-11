from statsmodels.nonparametric.kernel_density import KDEMultivariate

from .make_mesh_grid_coordinates_per_axis import make_mesh_grid_coordinates_per_axis


def estimate_kernel_density(
    coordinates,
    variable_types=None,
    bandwidths="cv_ml",
    mins=None,
    maxs=None,
    grid_sizes=None,
):

    n_dimension = len(coordinates)

    if variable_types is None:

        variable_types = "c" * n_dimension

    kde_multivariate = KDEMultivariate(
        coordinates, var_type=variable_types, bw=bandwidths
    )

    if mins is None:

        mins = tuple(coordinate.min() for coordinate in coordinates)

    if maxs is None:

        maxs = tuple(coordinate.max() for coordinate in coordinates)

    if grid_sizes is None:

        grid_sizes = (64,) * n_dimension

    return kde_multivariate.pdf(
        make_mesh_grid_coordinates_per_axis(mins, maxs, grid_sizes)
    ).reshape(grid_sizes)
