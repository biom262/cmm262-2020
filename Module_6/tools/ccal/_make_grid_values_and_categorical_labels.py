from numpy import full, nan, rot90, unique

from .compute_bandwidths import compute_bandwidths
from .estimate_kernel_density import estimate_kernel_density


def _make_grid_values_and_categorical_labels(
    element_x_dimension, element_labels, n_grid, bandwidth_factor, mask
):

    n_dimension = element_x_dimension.shape[1]

    variable_types = "c" * n_dimension

    global_bandwidths = compute_bandwidths(
        tuple(
            element_x_dimension[:, dimension_index]
            for dimension_index in range(n_dimension)
        ),
        variable_types,
    )

    global_bandwidths *= bandwidth_factor

    label_grid_probabilities = {}

    mins = (0,) * n_dimension

    maxs = (1,) * n_dimension

    grid_sizes = (n_grid,) * n_dimension

    for label in unique(element_labels):

        variables = tuple(
            element_x_dimension[element_labels == label][:, dimension_index]
            for dimension_index in range(n_dimension)
        )

        kernel_density = rot90(
            estimate_kernel_density(
                variables,
                variable_types,
                bandwidths=global_bandwidths,
                mins=mins,
                maxs=maxs,
                grid_sizes=grid_sizes,
            )
        )

        label_grid_probabilities[label] = kernel_density / kernel_density.sum()

    shape = (n_grid,) * n_dimension

    grid_values = full(shape, nan)

    grid_labels = full(shape, nan)

    for i in range(n_grid):

        for j in range(n_grid):

            if not mask[i, j]:

                max_probability = 0

                max_label = nan

                for label, grid_probabilities in label_grid_probabilities.items():

                    probability = grid_probabilities[i, j]

                    if max_probability < probability:

                        max_probability = probability

                        max_label = label

                grid_values[i, j] = max_probability

                grid_labels[i, j] = max_label

    return grid_values, grid_labels
