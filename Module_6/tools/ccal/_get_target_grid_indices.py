from numpy import apply_along_axis, linspace, meshgrid


def _get_target_grid_indices(nd_array, function):

    return tuple(
        meshgrid_.astype(int).ravel()
        for meshgrid_ in meshgrid(
            *(
                linspace(0, nd_array.shape[i] - 1, nd_array.shape[i])
                for i in range(nd_array.ndim - 1)
            ),
            indexing="ij",
        )
    ) + (apply_along_axis(function, nd_array.ndim - 1, nd_array).ravel(),)
