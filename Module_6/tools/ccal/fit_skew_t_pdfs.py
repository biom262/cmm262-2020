from pandas import concat

from ._fit_skew_t_pdfs import _fit_skew_t_pdfs
from .multiprocess import multiprocess
from .split_df import split_df


def fit_skew_t_pdfs(df, n_job=1, output_file_path=None):

    skew_t_pdf_fit_parameter = concat(
        multiprocess(
            _fit_skew_t_pdfs,
            ((df_,) for df_ in split_df(df, 0, min(df.shape[0], n_job))),
            n_job,
        )
    )

    if output_file_path is not None:

        skew_t_pdf_fit_parameter.to_csv(output_file_path, sep="\t")

    return skew_t_pdf_fit_parameter
