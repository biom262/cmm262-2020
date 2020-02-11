from numpy import log


def compute_entropy(array_1d):

    probability = array_1d / array_1d.sum()

    return -(probability * log(probability)).sum()
