from scipy.spatial.distance import pdist, squareform
from sklearn.manifold import MDS


def mds(
    n_target_dimension,
    point_x_dimension=None,
    distance_function="euclidean",
    distance__point_x_point=None,
    metric=True,
    n_init=int(1e3),
    max_iter=int(1e3),
    verbose=0,
    eps=1e-3,
    n_job=1,
    random_seed=20121020,
):

    if isinstance(distance_function, str) and distance__point_x_point is None:

        mds_ = MDS(
            n_components=n_target_dimension,
            dissimilarity=distance_function,
            metric=metric,
            n_init=n_init,
            max_iter=max_iter,
            verbose=verbose,
            eps=eps,
            n_jobs=n_job,
            random_state=random_seed,
        )

        point_x_target_dimension = mds_.fit_transform(point_x_dimension)

    else:

        mds_ = MDS(
            n_components=n_target_dimension,
            dissimilarity="precomputed",
            metric=metric,
            n_init=n_init,
            max_iter=max_iter,
            verbose=verbose,
            eps=eps,
            n_jobs=n_job,
            random_state=random_seed,
        )

        if distance__point_x_point is None:

            distance__point_x_point = squareform(
                pdist(point_x_dimension, distance_function)
            )

        point_x_target_dimension = mds_.fit_transform(distance__point_x_point)

    return point_x_target_dimension
