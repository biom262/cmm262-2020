def get_vcf_info(info, field):

    for info_ in info.split(sep=";"):

        if "=" in info_:

            info_field, info_value = info_.split(sep="=")

            if info_field == field:

                return info_value
