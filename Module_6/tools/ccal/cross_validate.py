from numpy import full, nan
from sklearn.model_selection import KFold


def cross_validate(model, sample_x_feature, sample_class, n_partition, scoring_funcion):

    scores = full(n_partition, nan)

    for i, (training_indices, testing_indices) in enumerate(
        KFold(n_splits=n_partition).split(sample_x_feature, sample_class)
    ):

        model.fit(sample_x_feature[training_indices, :], sample_class[training_indices])

        scores[i] = scoring_funcion(
            model.predict(sample_x_feature[testing_indices, :]),
            sample_class[testing_indices],
        )

    return scores
