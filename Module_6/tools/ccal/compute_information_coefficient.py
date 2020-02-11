import rpy2.robjects as ro
from numpy import asarray, exp, finfo, isnan, log, nan, sign, sqrt, unique
from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects.packages import importr
from scipy.stats import pearsonr

eps = finfo(float).eps

ro.conversion.py2ri = numpy2ri

mass = importr("MASS")


def compute_information_coefficient(x, y, n_grid=24):

    pearson_correlation = pearsonr(x, y)[0]

    if isnan(pearson_correlation) or unique(x).size == 1 or unique(y).size == 1:

        return nan

    else:

        pearson_correlation_abs = abs(pearson_correlation)

        bandwidth_x = mass.bcv(x)[0] * (1 - pearson_correlation_abs * 0.75)

        bandwidth_y = mass.bcv(y)[0] * (1 - pearson_correlation_abs * 0.75)

        fxy = (
            asarray(
                mass.kde2d(
                    x, y, asarray((bandwidth_x, bandwidth_y)), n=asarray((n_grid,))
                )[2]
            )
            + eps
        )

        dx = (x.max() - x.min()) / (n_grid - 1)

        dy = (y.max() - y.min()) / (n_grid - 1)

        pxy = fxy / (fxy.sum() * dx * dy)

        px = pxy.sum(axis=1) * dy

        py = pxy.sum(axis=0) * dx

        mi = (
            (
                pxy * log(pxy / (asarray((px,) * n_grid).T * asarray((py,) * n_grid)))
            ).sum()
            * dx
            * dy
        )

        # hxy = - (pxy * log(pxy)).sum() * dx * dy

        # hx = -(px * log(px)).sum() * dx

        # hy = -(py * log(py)).sum() * dy

        # mi = hx + hy - hxy

        return sign(pearson_correlation) * sqrt(1 - exp(-2 * mi))
