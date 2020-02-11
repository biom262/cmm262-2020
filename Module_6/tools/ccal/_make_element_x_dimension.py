from numpy import full, nan, sort

from .normalize_nd_array import normalize_nd_array


def _make_element_x_dimension(node_x_element, node_x_dimension, n_pull, pull_power):

    element_x_dimension = full(
        (node_x_element.shape[1], node_x_dimension.shape[1]), nan
    )

    node_x_element = normalize_nd_array(node_x_element, None, "0-1")

    for element_index in range(node_x_element.shape[1]):

        pulls = node_x_element[:, element_index]

        if 3 < pulls.size:

            pulls = normalize_nd_array(pulls, None, "0-1")

        if n_pull is not None:

            pulls[pulls < sort(pulls)[-n_pull]] = 0

        if pull_power is not None:

            pulls = pulls ** pull_power

        for dimension_index in range(node_x_dimension.shape[1]):

            element_x_dimension[element_index, dimension_index] = (
                pulls * node_x_dimension[:, dimension_index]
            ).sum() / pulls.sum()

    return element_x_dimension
