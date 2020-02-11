from numpy import full, nan
from pandas import DataFrame

from .single_sample_gsea import single_sample_gsea


def _single_sample_gseas(gene_x_sample,
                         gene_sets,
                         statistic,
                         alpha,
                         sample_norm_type):

    print("Running single-sample GSEA with {} gene sets ...".format(gene_sets.shape[0]))

    score__gene_set_x_sample = full((gene_sets.shape[0], gene_x_sample.shape[1]), nan)

    for sample_index, (sample_name, gene_score) in enumerate(gene_x_sample.items()):

        for gene_set_index, (gene_set_name, gene_set_genes) in enumerate(
            gene_sets.iterrows()):

            score__gene_set_x_sample[gene_set_index, sample_index] = single_sample_gsea(
                                                                                      gene_score,
                                                                                      gene_set_genes,
                                                                                      statistic=statistic,
                                                                                      alpha=alpha,
                                                                                      plot=False,
                                                                                      sample_norm_type = sample_norm_type)

    score__gene_set_x_sample = DataFrame(
        score__gene_set_x_sample, index=gene_sets.index, columns=gene_x_sample.columns
    )

    return score__gene_set_x_sample
