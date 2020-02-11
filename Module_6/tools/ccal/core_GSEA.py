from warnings import warn

from numpy import absolute, in1d, asarray, round

from ._plot_mountain import _plot_mountain
import sys

def core_GSEA(
    gene_score,
    gene_set_genes,
    statistic="ks",
    alpha=1.0,
    plot=False,
    plot_gene_names = False,
    title=None,
    gene_score_name=None,
    annotation_text_font_size=12,
    annotation_text_width=100,
    annotation_text_yshift=50,
    html_file_path=None,
    sample_norm_type = None,
    plotly_html_file_path=None,
):

    if sample_norm_type == 'rank':
        gene_score = gene_score.rank(method='average', numeric_only=None, na_option='keep', ascending=True, pct=False)
        gene_score = 10000 * (gene_score - gene_score.min())/(gene_score.max() - gene_score.min())
    elif sample_norm_type == 'zscore':
        gene_score = (gene_score - gene_score.mean())/gene_score.std()
    elif sample_norm_type is not None:
        sys.exit('ERROR: unknown sample_norm_type: {}'.format(sample_norm_type))
        
    gene_score_sorted = gene_score.sort_values(ascending=False)
    
    gene_set_gene_None = {gene_set_gene: None for gene_set_gene in gene_set_genes}

    in_ = asarray(
        [
            gene_score_gene in gene_set_gene_None
            #for gene_score_gene in gene_score.index.values
            for gene_score_gene in gene_score_sorted.index.values
        ],
        dtype=int,
    )

    #print(in_) 
    #print(gene_score_sorted)
    
    up = in_ * absolute(gene_score_sorted.values)**alpha
    up /= up.sum()
    down = 1.0 - in_
    down /= down.sum()
    cumsum = (up - down).cumsum()
    up_CDF = up.cumsum()
    down_CDF = down.cumsum()

    if statistic == "ks":

        max_ = cumsum.max()
        min_ = cumsum.min()
        if absolute(min_) < absolute(max_):
            gsea_score = max_
        else:
            gsea_score = min_
            
    elif statistic == "auc":
        gsea_score = cumsum.sum()

    gsea_score = round(gsea_score, 3)
        
    if plot:
        
        _plot_mountain(
            up_CDF,
            down_CDF,
            cumsum,
            in_,
            gene_score_sorted,
            gsea_score,
            None,
            None,
            title,
            gene_score_name,
            annotation_text_font_size,
            annotation_text_width,
            annotation_text_yshift,
            plot_gene_names,
            html_file_path,
            plotly_html_file_path,
        )

    return gsea_score
