from pandas import DataFrame, Index
from scipy.spatial.distance import pdist, squareform

from .establish_path import establish_path
from .hierarchical_consensus_cluster import hierarchical_consensus_cluster
from .multiprocess import multiprocess
from .plot_heat_map import plot_heat_map
from .plot_points import plot_points


def hierarchical_consensus_cluster_with_ks(
    df,
    ks,
    n_job=1,
    distance__column_x_column=None,
    distance_function="euclidean",
    n_clustering=10,
    random_seed=20121020,
    linkage_method="ward",
    plot_df=True,
    directory_path=None,
):

    if directory_path is None:

        k_directory_paths = tuple(None for k in ks)

    else:

        k_directory_paths = tuple("{}/{}".format(directory_path, k) for k in ks)

        for k_directory_path in k_directory_paths:

            establish_path(k_directory_path, "directory")

    k_return = {}

    if distance__column_x_column is None:

        print("Computing distance with {} ...".format(distance_function))

        distance__column_x_column = DataFrame(
            squareform(pdist(df.values.T, distance_function)),
            index=df.columns,
            columns=df.columns,
        )

    if directory_path is not None:

        distance__column_x_column.to_csv(
            "{}/distance.column_x_column.tsv".format(directory_path), sep="\t"
        )

    for k, (column_cluster, column_cluster__ccc) in zip(
        ks,
        multiprocess(
            hierarchical_consensus_cluster,
            (
                (
                    df,
                    k,
                    distance__column_x_column,
                    None,
                    n_clustering,
                    random_seed,
                    linkage_method,
                    plot_df,
                    k_directory_path,
                )
                for k, k_directory_path in zip(ks, k_directory_paths)
            ),
            n_job=n_job,
        ),
    ):

        k_return["K{}".format(k)] = {
            "column_cluster": column_cluster,
            "column_cluster.ccc": column_cluster__ccc,
        }

    keys = Index(("K{}".format(k) for k in ks), name="K")

    file_name = "hcc.column_cluster.ccc.html"

    if directory_path is None:

        html_file_path = None

    else:

        html_file_path = "{}/{}".format(directory_path, file_name)

    plot_points(
        (ks,),
        (tuple(k_return[key]["column_cluster.ccc"] for key in keys),),
        names=("Column Cluster CCC",),
        modes=("lines+markers",),
        title="HCC Column Cluster CCC",
        xaxis_title="K",
        yaxis_title="CCC",
        html_file_path=html_file_path,
    )

    k_x_column = DataFrame(
        [k_return[key]["column_cluster"] for key in keys],
        index=keys,
        columns=df.columns,
    )

    if directory_path is not None:

        k_x_column.to_csv("{}/hcc.k_x_column.tsv".format(directory_path), sep="\t")

    if plot_df:

        file_name = "hcc.k_x_column.distribution.html"

        if directory_path is None:

            html_file_path = None

        else:

            html_file_path = "{}/{}".format(directory_path, file_name)

        plot_heat_map(
            k_x_column,
            sort_axis=1,
            colorscale="COLOR_CATEGORICAL",
            title="HCC Column Cluster Distribution",
            xaxis_title=k_x_column.columns.name,
            yaxis_title=k_x_column.index.name,
            html_file_path=html_file_path,
        )

    return k_return
