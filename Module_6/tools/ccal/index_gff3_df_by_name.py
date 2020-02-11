from numpy import sort
from pandas import concat

from .get_gff3_attribute import get_gff3_attribute


def index_gff3_df_by_name(gff3_df):

    df = gff3_df.copy()

    print("GFF3 Shape: {}.".format(df.shape))

    df["Name"] = df["attributes"].map(
        lambda attribute: get_gff3_attribute(attribute, "Name")
    )

    df_without_duplicated_names = df.drop_duplicates(subset="Name", keep=False)

    print(
        "GFF3 Shape (without duplicated names {}): {}.".format(
            ", ".join(sort(df["Name"][df["Name"].duplicated()].unique())),
            df_without_duplicated_names.shape,
        )
    )

    rescued = []

    for name, df_ in df.groupby("Name"):

        if 1 < df_.shape[0]:

            versions = df_["attributes"].map(
                lambda attribute: get_gff3_attribute(attribute, "version")
            )

            rescued.append(df_.loc[versions.astype(int).idxmax()])

    df = (
        concat((df_without_duplicated_names, concat(rescued, axis=1).T))
        .sort_index()
        .set_index("Name")
    )

    print("GFF3 Shape (after rescuing duplicated names): {}.".format(df.shape))

    return df
