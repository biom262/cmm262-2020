from pandas import concat

from ._ssGSEA import _ssGSEA
from .multiprocess import multiprocess
from .split_df import split_df


def ssGSEA(
    gene_x_sample,
    gene_sets,
    statistic="ks",
    alpha=1.0,
    n_job=1,
    file_path=None,
    sample_norm_type = None):

    score__gene_set_x_sample = concat(
        multiprocess(
            _ssGSEA,
            (
                (gene_x_sample, gene_sets_, statistic, alpha, sample_norm_type)
                for gene_sets_ in split_df(gene_sets, 0, min(gene_sets.shape[0], n_job))
            ),
            n_job,
        )
    )

    if file_path is not None:

        score__gene_set_x_sample.to_csv(file_path, sep="\t")

    return score__gene_set_x_sample
 
