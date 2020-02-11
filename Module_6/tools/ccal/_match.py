from numpy import array_split, concatenate
from pandas import DataFrame

from ._match_randomly_sampled_target_and_data_to_compute_margin_of_errors import (
    _match_randomly_sampled_target_and_data_to_compute_margin_of_errors,
)
from ._match_target_and_data import _match_target_and_data
from ._permute_target_and_match_target_and_data import (
    _permute_target_and_match_target_and_data,
)
from .compute_empirical_p_values_and_fdrs import compute_empirical_p_values_and_fdrs
from .multiprocess import multiprocess
from .select_series_indices import select_series_indices


def _match(
    target,
    data,
    n_job,
    match_function,
    n_required_for_match_function,
    raise_for_n_less_than_required,
    n_extreme,
    fraction_extreme,
    random_seed,
    n_sampling,
    n_permutation,
):

    score_moe_p_value_fdr = DataFrame(columns=("Score", "0.95 MoE", "P-Value", "FDR"))

    n_job = min(data.shape[0], n_job)

    print(
        "Computing score using {} with {} process ...".format(
            match_function.__name__, n_job
        )
    )

    data_split = array_split(data, n_job)

    score_moe_p_value_fdr["Score"] = concatenate(
        multiprocess(
            _match_target_and_data,
            (
                (
                    target,
                    data_,
                    match_function,
                    n_required_for_match_function,
                    raise_for_n_less_than_required,
                )
                for data_ in data_split
            ),
            n_job,
        )
    )

    indices = select_series_indices(
        score_moe_p_value_fdr["Score"],
        "<>",
        n=n_extreme,
        fraction=fraction_extreme,
        plot=False,
    )

    score_moe_p_value_fdr.loc[
        indices, "0.95 MoE"
    ] = _match_randomly_sampled_target_and_data_to_compute_margin_of_errors(
        target,
        data[indices],
        random_seed,
        n_sampling,
        match_function,
        n_required_for_match_function,
        raise_for_n_less_than_required,
    )

    p_values, fdrs = compute_empirical_p_values_and_fdrs(
        score_moe_p_value_fdr["Score"],
        concatenate(
            multiprocess(
                _permute_target_and_match_target_and_data,
                (
                    (
                        target,
                        data_,
                        random_seed,
                        n_permutation,
                        match_function,
                        n_required_for_match_function,
                        raise_for_n_less_than_required,
                    )
                    for data_ in data_split
                ),
                n_job,
            )
        ).flatten(),
        "<>",
        raise_for_bad=False,
    )

    score_moe_p_value_fdr["P-Value"] = p_values

    score_moe_p_value_fdr["FDR"] = fdrs

    return score_moe_p_value_fdr
