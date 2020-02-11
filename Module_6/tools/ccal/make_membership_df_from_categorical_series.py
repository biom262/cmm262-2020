from pandas import DataFrame


def make_membership_df_from_categorical_series(series):

    object_x_index = DataFrame(index=sorted(set(series.dropna())), columns=series.index)

    object_x_index.index.name = series.name

    for object_ in object_x_index.index:

        object_x_index.loc[object_] = (series == object_).astype(int)

    return object_x_index
