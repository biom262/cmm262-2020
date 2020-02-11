from numpy import exp, full, nan
from numpy.random import choice, normal, random_sample, seed
from scipy.spatial import Delaunay
from scipy.spatial.distance import euclidean, pdist, squareform
from scipy.stats import pearsonr

from .apply_function_on_2_2d_arrays_slices import apply_function_on_2_2d_arrays_slices
from .plot_points import plot_points


def _anneal_node_and_element_positions(
    distance__node_x_node,
    distance__element_x_element,
    distance__node_x_element,
    node_x_dimension,
    element_x_dimension,
    node_node_score_weight,
    element_element_score_weight,
    node_element_score_weight,
    n_fraction_node_to_move,
    n_fraction_element_to_move,
    random_seed,
    n_iteration,
    initial_temperature,
    scale,
    triangulate,
    print_acceptance,
):

    target_distance__node_x_node = squareform(distance__node_x_node)

    target_distance__element_x_element = squareform(distance__element_x_element)

    target_distance__node_x_element = distance__node_x_element.ravel()

    scores = full((n_iteration, 5), nan)

    node_x_node_score = pearsonr(pdist(node_x_dimension), target_distance__node_x_node)[
        0
    ]

    element_x_element_score = pearsonr(
        pdist(element_x_dimension), target_distance__element_x_element
    )[0]

    node_x_element_score = pearsonr(
        apply_function_on_2_2d_arrays_slices(
            node_x_dimension, element_x_dimension, euclidean, 1
        ).ravel(),
        target_distance__node_x_element,
    )[0]

    fitness = (
        node_x_node_score * node_node_score_weight
        + element_x_element_score * element_element_score_weight
        + node_x_element_score * node_element_score_weight
    )

    n_node = distance__node_x_node.shape[0]

    n_node_to_move = int(n_node * n_fraction_node_to_move)

    n_element = distance__element_x_element.shape[0]

    n_element_to_move = int(n_element * n_fraction_element_to_move)

    n_per_print = max(1, n_iteration // 10)

    seed(random_seed)

    for i in range(n_iteration):

        if i % n_per_print == 0:

            print("\t{}/{} ...".format(i + 1, n_iteration))

        r__node_x_dimension = node_x_dimension.copy()

        indices = choice(range(n_node), size=n_node_to_move, replace=True)

        r__node_x_dimension[indices] = normal(r__node_x_dimension[indices], scale=scale)

        if triangulate:

            n_triangulation = Delaunay(r__node_x_dimension)

        r__element_x_dimension = element_x_dimension.copy()

        for index in choice(range(n_element), size=n_element_to_move, replace=True):

            element_x_y = r__element_x_dimension[index]

            r__element_x_y = normal(element_x_y, scale=scale)

            if triangulate:

                while n_triangulation.find_simplex(r__element_x_y) == -1:

                    r__element_x_y = normal(element_x_y, scale=scale)

            r__element_x_dimension[index] = r__element_x_y

        r__node_x_node_score = pearsonr(
            pdist(r__node_x_dimension), target_distance__node_x_node
        )[0]

        r__element_x_element_score = pearsonr(
            pdist(r__element_x_dimension), target_distance__element_x_element
        )[0]

        r__node_x_element_score = pearsonr(
            apply_function_on_2_2d_arrays_slices(
                r__node_x_dimension, r__element_x_dimension, euclidean, 1
            ).ravel(),
            target_distance__node_x_element,
        )[0]

        r__fitness = (
            r__node_x_node_score * node_node_score_weight
            + r__element_x_element_score * element_element_score_weight
            + r__node_x_element_score * node_element_score_weight
        )

        temperature = initial_temperature * (1 - i / (n_iteration + 1))

        if random_sample() < exp((r__fitness - fitness) / temperature):

            if print_acceptance:

                print("\t\t{:.3e} =(accept)=> {:.3e} ...".format(fitness, r__fitness))

            node_x_dimension = r__node_x_dimension

            element_x_dimension = r__element_x_dimension

            node_x_node_score = r__node_x_node_score

            element_x_element_score = r__element_x_element_score

            node_x_element_score = r__node_x_element_score

            fitness = r__fitness

        scores[i, :] = (
            temperature,
            node_x_node_score,
            element_x_element_score,
            node_x_element_score,
            fitness,
        )

    plot_points(
        tuple(tuple(range(n_iteration)) for i in range(scores.shape[1])),
        tuple(scores[:, i] for i in range(scores.shape[1])),
        names=(
            "Temperature",
            "Node-Node",
            "Element-Element",
            "Node-Element",
            "Fitness",
        ),
    )

    return node_x_dimension, element_x_dimension
