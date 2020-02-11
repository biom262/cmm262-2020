def _identify_what_to_count(signature_component_weight):

    signature_component_dict = {}

    signature_component_differing_dict = {}

    signature_component_before_dict = {}

    signature_component_before_differing_dict = {}

    for signature_component, weight in signature_component_weight.items():

        signature_component_before, signature_component_after = signature_component.split(
            " ==> "
        )

        signature_component_dict[signature_component] = {
            "before_sequence": signature_component_before,
            "after_sequence": signature_component_after,
            "n": 0,
            "weight": weight,
        }

        signature_component_before_differing = signature_component_before[1]

        signature_component_after_differing = signature_component_after[1]

        k = "{} ==> {}".format(
            signature_component_before_differing, signature_component_after_differing
        )

        if k not in signature_component_differing_dict:

            signature_component_differing_dict[k] = {
                "before_sequence": signature_component_before_differing,
                "after_sequence": signature_component_after_differing,
                "n": 0,
                "weight": weight,
            }

        else:

            signature_component_differing_dict[k]["weight"] = max(
                weight, signature_component_differing_dict[k]["weight"]
            )

        k = signature_component_before

        if k not in signature_component_before_dict:

            signature_component_before_dict[k] = {"n": 0, "weight": weight}

        else:

            signature_component_before_dict[k]["weight"] = max(
                weight, signature_component_before_dict[k]["weight"]
            )

        k = signature_component_before_differing

        if k not in signature_component_before_differing_dict:

            signature_component_before_differing_dict[k] = {"n": 0, "weight": weight}

        else:

            signature_component_before_differing_dict[k]["weight"] = max(
                weight, signature_component_before_differing_dict[k]["weight"]
            )

    return (
        signature_component_dict,
        signature_component_differing_dict,
        signature_component_before_dict,
        signature_component_before_differing_dict,
    )
