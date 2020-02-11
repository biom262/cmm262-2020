def clean_name(name):

    cleaned_name = ""

    for character in name:

        if character.isalnum():

            cleaned_name += character

        else:

            cleaned_name += "_"

    return cleaned_name
