def get_variant_type(ref, alt):

    if len(ref) == len(alt):

        if len(ref) == 1:

            variant_type = "SNP"

        elif len(ref) == 2:

            variant_type = "DNP"

        elif len(ref) == 3:

            variant_type = "TNP"

        else:

            variant_type = "ONP"

    elif len(ref) < len(alt):

        variant_type = "INS"

    else:

        variant_type = "DEL"

    return variant_type
