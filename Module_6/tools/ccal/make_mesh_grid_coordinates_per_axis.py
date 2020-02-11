from numpy import asarray, linspace, meshgrid

from .check_nd_array_for_bad import check_nd_array_for_bad


def make_mesh_grid_coordinates_per_axis(
    mins, maxs, grid_sizes, indexing="ij", raise_for_bad=True
):

    min_max_grid_size = asarray((mins, maxs, grid_sizes)).T

    check_nd_array_for_bad(min_max_grid_size, raise_for_bad=raise_for_bad)

    coordinates_by_axis = (
        linspace(min_, max_, num=grid_size)
        for min_, max_, grid_size in min_max_grid_size
    )

    return asarray(
        tuple(
            mesh_grid.ravel()
            for mesh_grid in meshgrid(*coordinates_by_axis, indexing=indexing)
        )
    )
