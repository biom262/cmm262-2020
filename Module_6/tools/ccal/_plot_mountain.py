from numpy import absolute, asarray

from .plot_and_save import plot_and_save

def _plot_mountain(
    up_CDF,
    down_CDF,    
    cumulative_sums,
    hits,
    gene_score,
    score,
    layout_width,
    layout_height,
    title,
    gene_score_name,
    annotation_text_font_size,
    annotation_text_width,
    annotation_text_yshift,
    plot_gene_names,
    html_file_path,
    plotly_html_file_path):

    if title is None:

        title = "GSEA Enrichment Plot"

    if gene_score_name is None:

        gene_score_name = "Gene Score"

    layout = dict(
        width=layout_width,
        height=layout_height,
        hovermode="closest",
        title=title,
        xaxis=dict(anchor="y", title="Gene Rank"),
        yaxis=dict(domain=(0, 0.16), title=gene_score_name),
        yaxis2=dict(domain=(0.20, 1), title="Enrichment"),
        legend=dict(orientation="v"),
    )

    data = []
    data2 = []

    grid = asarray(range(cumulative_sums.size))

    line_width = 3.2

    data.append(
        dict(
            yaxis="y2",
            type="scatter",
            name="Running Enrichment",
            x=grid,
            y=cumulative_sums,
            line=dict(width=line_width, color="#20d9ba"),
            fill="tozeroy"))

    # This is a temporary addition to make pedagogical plots
    #data2.append(
    #    dict(
    #        yaxis="y2",
    #        type="scatter",
    #        name="Running Enrichment",
    #        x=grid,
    #        y=up_CDF,
    #        line=dict(width=line_width, color="#20d9ba"),
    #        fill="tozeroy"))
    #data2.append(
    #    dict(
    #        yaxis="y2",
    #        type="scatter",
    #        name="Running Enrichment",
    #        x=grid,
    #        y=down_CDF,
    #        line=dict(width=line_width, color="#20d9ba"),
    #        fill="tozeroy"))
    
    cumulative_sums_argmax = absolute(cumulative_sums).argmax()

    negative_color = "#4e40d8"

    positive_color = "#ff1968"

    data.append(
        dict(
            yaxis="y2",
            type="scatter",
            name="Peak",
            x=(grid[cumulative_sums_argmax],),
            y=(cumulative_sums[cumulative_sums_argmax],),
            mode="markers",
            marker=dict(size=16, color=(negative_color, positive_color)[0 <= score])))

    gene_xs = tuple(i for i in grid if hits[i])
    gene_xs_misses = tuple(i for i in grid if hits[i] == 0)
    
    gene_texts = tuple("<b>{}</b>".format(text) for text in gene_score.index[hits == 1])

    data.append(
        dict(
            yaxis="y2",
            type="scatter",
            name="Genes in Gene Set",
            x=gene_xs,
            y=(0,) * len(gene_xs),
            text=gene_texts,
            mode="markers",
            marker=dict(
                symbol="line-ns-open",
                size=12,
                color="#9017e6",
                line=dict(width=line_width)),
                hoverinfo="x+text"))

    #data2.append(
    #    dict(
    #        yaxis="y2",
    #        type="scatter",
    #        name="Genes in Gene Set",
    #        x=gene_xs,
    #        y=(0,) * len(gene_xs),
    #        text=gene_texts,
    #        mode="markers",
    #        marker=dict(
    #            symbol="line-ns-open",
    #            size=12,
    #            color="#9017e6",
    #            line=dict(width=line_width)),
    #            hoverinfo="x+text"))
    #data2.append(
    #    dict(
    #        yaxis="y2",
    #        type="scatter",
    #        name="Genes Not in Gene Set",
    #        x=gene_xs_misses,
    #        y=(0,) * len(gene_xs_misses),
    #        #text=gene_texts,
    #        mode="markers",
    #        marker=dict(
    #            symbol="line-ns-open",
    #            size=12,
    #            color="#999999",
    #            line=dict(width=line_width)),
    #            hoverinfo="x+text"))


    
    is_negative = gene_score < 0

    for indices, color, name in (
        (is_negative, negative_color, 'Negative Gene Score'),
        (~is_negative, positive_color, 'Positive Gene Score')):

        data.append(
            dict(
                type="scatter",
                name=name,
                legendgroup="Gene Score",
                x=grid[indices],
                y=gene_score[indices],
                line=dict(width=line_width, color=color),
                fill="tozeroy"))

        #data2.append(
        #    dict(
        #        type="scatter",
        #        name=name,
        #        legendgroup="Gene Score",
        #        x=grid[indices],
        #        y=gene_score[indices],
        #        line=dict(width=line_width, color=color),
        #        fill="tozeroy"))
        
    layout["annotations"] = [
        dict(
            xref="paper",
            yref="paper",
            x=0.5,
            y=1.05,
            text="<b>Enrichment Score = {:.3f}</b>".format(score),
            showarrow=False,
            font=dict(size=16, color=(negative_color, positive_color)[0 <= score]),
            bgcolor='#ffffff',
            borderpad=3.2)]

    if plot_gene_names == True:

        layout["annotations"] = layout["annotations"] + [
            dict(
                x=x,
                y=0,
                yref="y2",
                clicktoshow="onoff",
                text=text,
                showarrow=False,
                font=dict(size=annotation_text_font_size),
                textangle=-90,
                width=annotation_text_width,
                borderpad=0,
                yshift=-annotation_text_yshift) 
            for i, (x, text) in enumerate(zip(gene_xs, gene_texts))]

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)

    #plot_and_save(dict(layout=layout, data=data2), html_file_path, plotly_html_file_path)
