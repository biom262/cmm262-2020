from numpy import full, nan
from pandas import DataFrame

from .fit_skew_t_pdf import fit_skew_t_pdf


def _fit_skew_t_pdfs(df):

    skew_t_pdf_fit_parameter = full((df.shape[0], 5), nan)

    n = df.shape[0]

    n_per_print = max(1, n // 10)

    for i, (index, series) in enumerate(df.iterrows()):

        if i % n_per_print == 0:

            print("({}/{}) {} ...".format(i + 1, n, index))

        _1d_array = series.values

        skew_t_pdf_fit_parameter[i] = fit_skew_t_pdf(_1d_array)

    return DataFrame(
        skew_t_pdf_fit_parameter,
        index=df.index,
        columns=("N Data", "Location", "Scale", "Degree of Freedom", "Shape"),
    )
