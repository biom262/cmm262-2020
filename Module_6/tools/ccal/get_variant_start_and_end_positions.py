def get_variant_start_and_end_positions(pos, ref, alt):

    if len(ref) == len(alt):

        start_position, end_position = pos, pos + len(alt) - 1

    elif len(ref) < len(alt):

        start_position, end_position = pos, pos + 1

    else:

        start_position, end_position = pos + 1, pos + len(ref) - len(alt)

    return start_position, end_position
