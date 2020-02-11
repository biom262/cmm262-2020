from numpy import absolute, isnan, where
from scipy.spatial.distance import correlation


def compute_correlation_distance(x, y):

    correlation_distance = correlation(x, y)

    if isnan(correlation_distance):

        return 2

    else:

        return where(absolute(correlation_distance) < 1e-8, 0, correlation_distance)
