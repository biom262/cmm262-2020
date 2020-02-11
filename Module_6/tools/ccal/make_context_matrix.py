from pandas import concat

from ._make_context_matrix import _make_context_matrix
from .multiprocess import multiprocess
from .split_df import split_df


def make_context_matrix(
    df,
    n_job=1,
    skew_t_pdf_fit_parameter=None,
    n_grid=1e3,
    degree_of_freedom_for_tail_reduction=1e8,
    multiply_distance_from_reference_argmax=False,
    global_location=None,
    global_scale=None,
    global_degree_of_freedom=None,
    global_shape=None,
    output_file_path=None,
):

    context_matrix = concat(
        multiprocess(
            _make_context_matrix,
            (
                (
                    df_,
                    skew_t_pdf_fit_parameter,
                    n_grid,
                    degree_of_freedom_for_tail_reduction,
                    multiply_distance_from_reference_argmax,
                    global_location,
                    global_scale,
                    global_degree_of_freedom,
                    global_shape,
                )
                for df_ in split_df(df, 0, min(df.shape[0], n_job))
            ),
            n_job,
        )
    )

    context_matrix.to_csv(output_file_path, sep="\t")

    return context_matrix
