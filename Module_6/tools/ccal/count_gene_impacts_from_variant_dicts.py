def count_gene_impacts_from_variant_dicts(variant_dicts, gene_name):

    impact_counts = {"HIGH": 0, "MODERATE": 0, "LOW": 0, "MODIFIER": 0}

    for variant_dict in variant_dicts:

        if variant_dict["gene_name"] == gene_name:

            impact_counts[variant_dict["impact"]] += 1

    return impact_counts
