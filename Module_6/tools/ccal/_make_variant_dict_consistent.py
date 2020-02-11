def _make_variant_dict_consistent(
    variant_dict, ann_fields=("effect", "impact", "gene_name"), format_fields=("GT",)
):

    variant_dict["ANN"] = {
        0: {ann_field: variant_dict.get(ann_field) for ann_field in ann_fields}
    }

    variant_dict["sample"] = {
        0: {
            format_field: variant_dict.get(format_field)
            for format_field in format_fields
        }
    }
