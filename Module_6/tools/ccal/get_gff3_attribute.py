def get_gff3_attribute(attributes, field):

    for field_value in attributes.split(sep=";"):

        field_, value = field_value.split(sep="=")

        if field_ == field:

            return value
