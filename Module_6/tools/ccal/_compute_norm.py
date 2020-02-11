from numpy.linalg import norm


def _compute_norm(M):

    return norm(M, ord="fro")
