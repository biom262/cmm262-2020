def title_str(str_):

    original_uppers = []

    on_upper = False

    upper_start = upper_end = None

    for i, character in enumerate(str_):

        if character.isupper():

            if on_upper:

                upper_end += 1

            else:

                on_upper = True

                upper_start = i

                upper_end = upper_start + 1

        else:

            if on_upper:

                on_upper = False

                original_uppers.append((upper_start, upper_end))

                upper_start = upper_end = None

    if upper_start:

        original_uppers.append((upper_start, upper_end))

    str_ = str_.title().replace("_", " ")

    for upper_start, upper_end in original_uppers:

        str_ = (
            str_[:upper_start] + str_[upper_start:upper_end].upper() + str_[upper_end:]
        )

    for lowercase_character in (
        "a",
        "an",
        "the",
        "and",
        "but",
        "or",
        "for",
        "nor",
        "on",
        "at",
        "to",
        "from",
        "of",
        "vs",
    ):

        str_ = str_.replace(
            " {} ".format(lowercase_character.title()),
            " {} ".format(lowercase_character),
        )

    return " ".join(sub_str.strip() for sub_str in str_.split())
