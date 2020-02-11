def split_str_ignoring_inside_quotes(str_, separator):

    splits = []

    part = ""

    for str_split in str_.split(separator):

        if '"' in str_split:

            if part:

                part += str_split

                splits.append(part)

                part = ""

            else:

                part = str_split

        else:

            if part:

                part += str_split

            else:

                splits.append(str_split)

    if part:

        splits.append(part)

    return splits
