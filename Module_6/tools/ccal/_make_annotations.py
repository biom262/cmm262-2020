from pandas import DataFrame


def _make_annotations(score_moe_p_value_fdr):

    annotations = DataFrame(index=score_moe_p_value_fdr.index)

    if score_moe_p_value_fdr["0.95 MoE"].isna().all():

        annotations["Score"] = score_moe_p_value_fdr["Score"].apply("{:.2f}".format)

    else:

        annotations["Score(\u0394)"] = score_moe_p_value_fdr[
            ["Score", "0.95 MoE"]
        ].apply(lambda score_moe: "{:.2f}({:.2f})".format(*score_moe), axis=1)

    if not score_moe_p_value_fdr["P-Value"].isna().all():

        function = "{:.2e}".format

        annotations["P-Value"] = score_moe_p_value_fdr["P-Value"].apply(function)

        annotations["FDR"] = score_moe_p_value_fdr["FDR"].apply(function)

    return annotations
