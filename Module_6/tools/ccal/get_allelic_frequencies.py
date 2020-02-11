def get_allelic_frequencies(ad, dp):

    return [int(allelic_depth) / int(dp) for allelic_depth in ad.split(sep=",")]
