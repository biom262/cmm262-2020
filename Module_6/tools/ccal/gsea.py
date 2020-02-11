from random import shuffle

from numpy import asarray, full, nan
from numpy.random import choice
from pandas import Series

from .compute_empirical_p_value import compute_empirical_p_value
from .single_sample_gsea import single_sample_gsea


def gsea(
    gene_x_sample,
    phenotypes,
    genes,
    function,
    statistic="ks",
    n_permutation=None,
    permuting="gene",
    plot=True,
    title=None,
    gene_score_name=None,
    annotation_text_font_size=16,
    annotation_text_width=88,
    annotation_text_yshift=64,
    html_file_path=None,
    plotly_html_file_path=None,
):

    print("Computing gene scores ...")

    gene_score = Series(
        gene_x_sample.apply(function, axis=1, args=(asarray(phenotypes),)),
        index=gene_x_sample.index,
    )

    print("Computing gene set {} enrichment ...".format(genes.name))

    score = single_sample_gsea(
        gene_score,
        genes,
        statistic=statistic,
        plot=plot,
        title=title,
        gene_score_name=gene_score_name,
        annotation_text_font_size=annotation_text_font_size,
        annotation_text_width=annotation_text_width,
        annotation_text_yshift=annotation_text_yshift,
        html_file_path=html_file_path,
        plotly_html_file_path=plotly_html_file_path,
    )

    if n_permutation is None:

        p_value = nan

    else:

        permutation_scores = full(n_permutation, nan)

        permuting__gene_x_sample = gene_x_sample.copy()

        permuting__phenotypes = asarray(phenotypes)

        for i in range(n_permutation):

            if permuting == "phenotype":

                shuffle(permuting__phenotypes)

            elif permuting == "gene":

                permuting__gene_x_sample.index = choice(
                    permuting__gene_x_sample.index,
                    size=permuting__gene_x_sample.shape[0],
                    replace=False,
                )

            permutation_scores[i] = single_sample_gsea(
                Series(
                    permuting__gene_x_sample.apply(
                        function, axis=1, args=(permuting__phenotypes,)
                    ),
                    index=permuting__gene_x_sample.index,
                ),
                genes,
                statistic=statistic,
                plot=False,
            )

        p_value = min(
            compute_empirical_p_value(score, permutation_scores, "<"),
            compute_empirical_p_value(score, permutation_scores, ">"),
        )

    return score, p_value
