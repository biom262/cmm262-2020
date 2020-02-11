from .compute_information_coefficient import compute_information_coefficient


def compute_information_distance(x, y, n_grid=24):

    return (1 - compute_information_coefficient(x, y, n_grid=n_grid)) / 2
