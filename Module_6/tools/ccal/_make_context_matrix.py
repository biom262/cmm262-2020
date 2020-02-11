from numpy import full, nan
from pandas import DataFrame

from .compute_context import compute_context


def _make_context_matrix(
    df,
    skew_t_pdf_fit_parameter,
    n_grid,
    degree_of_freedom_for_tail_reduction,
    multiply_distance_from_reference_argmax,
    global_location,
    global_scale,
    global_degree_of_freedom,
    global_shape,
):

    context_matrix = full(df.shape, nan)

    n = df.shape[0]

    n_per_print = max(1, n // 10)

    for i, (index, series) in enumerate(df.iterrows()):

        if i % n_per_print == 0:

            print("({}/{}) {} ...".format(i + 1, n, index))

        if skew_t_pdf_fit_parameter is None:

            n_data = location = scale = degree_of_freedom = shape = None

        else:

            n_data, location, scale, degree_of_freedom, shape = skew_t_pdf_fit_parameter.loc[
                index, ["N Data", "Location", "Scale", "Degree of Freedom", "Shape"]
            ]

        context_matrix[i] = compute_context(
            series.values,
            n_data=n_data,
            location=location,
            scale=scale,
            degree_of_freedom=degree_of_freedom,
            shape=shape,
            n_grid=n_grid,
            degree_of_freedom_for_tail_reduction=degree_of_freedom_for_tail_reduction,
            multiply_distance_from_reference_argmax=multiply_distance_from_reference_argmax,
            global_location=global_location,
            global_scale=global_scale,
            global_degree_of_freedom=global_degree_of_freedom,
            global_shape=global_shape,
        )["context_indices_like_array"]

    return DataFrame(context_matrix, index=df.index, columns=df.columns)
