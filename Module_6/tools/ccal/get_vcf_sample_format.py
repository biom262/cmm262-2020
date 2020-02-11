def get_vcf_sample_format(format_, sample, format_field):

    return sample.split(sep=":")[format_.split(sep=":").index(format_field)]
