def get_genotype(ref, alt, gt):

    return [
        ([ref] + alt.split(sep=","))[int(allelic_index)]
        for allelic_index in gt.replace("/", "|").split(sep="|")
    ]
