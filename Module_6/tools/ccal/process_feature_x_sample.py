from numpy import nan
from pandas import DataFrame

from .drop_df_slice import drop_df_slice
from .drop_df_slice_greedily import drop_df_slice_greedily
from .log_nd_array import log_nd_array
from .normalize_nd_array import normalize_nd_array
from .summarize_feature_x_sample import summarize_feature_x_sample


def process_feature_x_sample(
    feature_x_sample,
    features_to_drop=None,
    samples_to_drop=None,
    nanize=None,
    drop_axis=None,
    max_na=None,
    min_n_not_na_unique_value=None,
    shift_as_necessary_to_achieve_min_before_logging=None,
    log_base=None,
    normalization_axis=None,
    normalization_method=None,
    clip_min=None,
    clip_max=None,
    **summarize_feature_x_sample_kwargs,
):

    summarize_feature_x_sample(feature_x_sample, **summarize_feature_x_sample_kwargs)

    if feature_x_sample.index.has_duplicates:

        raise ValueError("{} duplicated.".format(feature_x_sample.index.name))

    elif feature_x_sample.columns.has_duplicates:

        raise ValueError("{} duplicated.".format(feature_x_sample.columns.name))

    shape_before_drop = feature_x_sample.shape

    if features_to_drop is not None:

        features_to_drop = feature_x_sample.index & set(features_to_drop)

        print(
            "Dropping {}: {} ...".format(feature_x_sample.index.name, features_to_drop)
        )

        feature_x_sample.drop(features_to_drop, inplace=True)

        print("Shape: {}".format(feature_x_sample.shape))

    if samples_to_drop is not None:

        samples_to_drop = feature_x_sample.columns & set(samples_to_drop)

        print(
            "Dropping {}: {} ...".format(
                feature_x_sample.columns.name, features_to_drop
            )
        )

        feature_x_sample.drop(samples_to_drop, axis=1, inplace=True)

        print("Shape: {}".format(feature_x_sample.shape))

    if feature_x_sample.shape != shape_before_drop:

        summarize_feature_x_sample(
            feature_x_sample, **summarize_feature_x_sample_kwargs
        )

    if nanize is not None:

        print("NANizing <= {} ...".format(nanize))

        feature_x_sample[feature_x_sample <= nanize] = nan

        summarize_feature_x_sample(
            feature_x_sample, **summarize_feature_x_sample_kwargs
        )

    if max_na is not None or min_n_not_na_unique_value is not None:

        if min_n_not_na_unique_value == "max":

            if drop_axis is None:

                min_n_not_na_unique_value = min(feature_x_sample.shape)

            else:

                min_n_not_na_unique_value = feature_x_sample.shape[drop_axis]

        print(
            "Dropping slice (drop_axis={} & max_na={} & min_n_not_na_unique_value={}) ...".format(
                drop_axis, max_na, min_n_not_na_unique_value
            )
        )

        shape_before_drop = feature_x_sample.shape

        if drop_axis is None:

            feature_x_sample = drop_df_slice_greedily(
                feature_x_sample,
                max_na=max_na,
                min_n_not_na_unique_value=min_n_not_na_unique_value,
            )

        else:

            feature_x_sample = drop_df_slice(
                feature_x_sample,
                drop_axis,
                max_na=max_na,
                min_n_not_na_unique_value=min_n_not_na_unique_value,
            )

        if feature_x_sample.shape != shape_before_drop:

            summarize_feature_x_sample(
                feature_x_sample, **summarize_feature_x_sample_kwargs
            )

    if log_base is not None:

        print(
            "Logging (shift_as_necessary_to_achieve_min_before_logging={} & log_base={}) ...".format(
                shift_as_necessary_to_achieve_min_before_logging, log_base
            )
        )

        feature_x_sample = DataFrame(
            log_nd_array(
                feature_x_sample.values,
                raise_for_bad=False,
                shift_as_necessary_to_achieve_min_before_logging=shift_as_necessary_to_achieve_min_before_logging,
                log_base=log_base,
            ),
            index=feature_x_sample.index,
            columns=feature_x_sample.columns,
        )

        summarize_feature_x_sample(
            feature_x_sample, **summarize_feature_x_sample_kwargs
        )

    if normalization_method is not None:

        print(
            "Axis-{} {} normalizing ...".format(
                normalization_axis, normalization_method
            )
        )

        feature_x_sample = DataFrame(
            normalize_nd_array(
                feature_x_sample.values,
                normalization_axis,
                normalization_method,
                raise_for_bad=False,
            ),
            index=feature_x_sample.index,
            columns=feature_x_sample.columns,
        )

        summarize_feature_x_sample(
            feature_x_sample, **summarize_feature_x_sample_kwargs
        )

    if clip_min is not None:

        print("|-{} clipping  ...".format(clip_min))

        feature_x_sample.clip(lower=clip_min, inplace=True)

    if clip_max is not None:

        print("{}-| clipping  ...".format(clip_max))

        feature_x_sample.clip(upper=clip_max, inplace=True)

    if clip_min is not None or clip_max is not None:

        summarize_feature_x_sample(
            feature_x_sample, **summarize_feature_x_sample_kwargs
        )

    return feature_x_sample
