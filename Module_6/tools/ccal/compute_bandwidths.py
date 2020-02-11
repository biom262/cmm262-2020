from statsmodels.nonparametric.kernel_density import KDEMultivariate


def compute_bandwidths(coordinates, variable_types, bandwidths="cv_ml"):

    return KDEMultivariate(coordinates, var_type=variable_types, bw=bandwidths).bw
