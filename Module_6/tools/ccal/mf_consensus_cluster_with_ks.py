from numpy import asarray
from pandas import DataFrame, Index

from .establish_path import establish_path
from .mf_consensus_cluster import mf_consensus_cluster
from .multiprocess import multiprocess
from .plot_heat_map import plot_heat_map
from .plot_points import plot_points


def mf_consensus_cluster_with_ks(
    df,
    ks,
    mf_function="nmf_by_sklearn",
    n_job=1,
    n_clustering=10,
    n_iteration=int(1e3),
    random_seed=20121020,
    linkage_method="ward",
    plot_w=True,
    plot_h=True,
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

    for (
        k,
        (
            w_0,
            h_0,
            e_0,
            w_element_cluster,
            w_element_cluster__ccc,
            h_element_cluster,
            h_element_cluster__ccc,
        ),
    ) in zip(
        ks,
        multiprocess(
            mf_consensus_cluster,
            (
                (
                    df,
                    k,
                    mf_function,
                    n_clustering,
                    n_iteration,
                    random_seed,
                    linkage_method,
                    plot_w,
                    plot_h,
                    plot_df,
                    k_directory_path,
                )
                for k, k_directory_path in zip(ks, k_directory_paths)
            ),
            n_job=n_job,
        ),
    ):

        k_return["K{}".format(k)] = {
            "w": w_0,
            "h": h_0,
            "e": e_0,
            "w_element_cluster": w_element_cluster,
            "w_element_cluster.ccc": w_element_cluster__ccc,
            "h_element_cluster": h_element_cluster,
            "h_element_cluster.ccc": h_element_cluster__ccc,
        }

    keys = Index(("K{}".format(k) for k in ks), name="K")

    file_name = "mf_error.html"

    if directory_path is None:

        html_file_path = None

    else:

        html_file_path = "{}/{}".format(directory_path, file_name)

    plot_points(
        (ks,),
        (tuple(k_return[key]["e"] for key in keys),),
        modes=("lines+markers",),
        title="MF Error",
        xaxis_title="K",
        yaxis_title="Error",
        html_file_path=html_file_path,
    )

    w_element_cluster__ccc = asarray(
        tuple(k_return[key]["w_element_cluster.ccc"] for key in keys)
    )

    h_element_cluster__ccc = asarray(
        tuple(k_return[key]["h_element_cluster.ccc"] for key in keys)
    )

    file_name = "mfcc.w_h_element_cluster.ccc.html"

    if directory_path is None:

        html_file_path = None

    else:

        html_file_path = "{}/{}".format(directory_path, file_name)

    plot_points(
        (ks,) * 3,
        (
            w_element_cluster__ccc,
            h_element_cluster__ccc,
            (w_element_cluster__ccc + h_element_cluster__ccc) / 2,
        ),
        names=("W Element Cluster CCC", "H Element Cluster CCC", "W H Mean"),
        modes=("lines+markers",) * 3,
        title="MFCC W H Element Cluster CCC",
        xaxis_title="K",
        yaxis_title="CCC",
        html_file_path=html_file_path,
    )

    for w_or_h, k_x_element in (
        (
            "w",
            DataFrame(
                [k_return[key]["w_element_cluster"] for key in keys],
                index=keys,
                columns=w_0.index,
            ),
        ),
        (
            "h",
            DataFrame(
                [k_return[key]["h_element_cluster"] for key in keys],
                index=keys,
                columns=h_0.columns,
            ),
        ),
    ):

        if directory_path is not None:

            k_x_element.to_csv(
                "{}/mfcc.k_x_{}_element.tsv".format(directory_path, w_or_h), sep="\t"
            )

        if plot_df:

            file_name = "mfcc.k_x_{}_element.distribution.html".format(w_or_h)

            if directory_path is None:

                html_file_path = None

            else:

                html_file_path = "{}/{}".format(directory_path, file_name)

            plot_heat_map(
                k_x_element,
                sort_axis=1,
                colorscale="COLOR_CATEGORICAL",
                title="MFCC {} Element Cluster Distribution".format(w_or_h.upper()),
                xaxis_title=k_x_element.columns.name,
                yaxis_title=k_x_element.index.name,
                html_file_path=html_file_path,
            )

    return k_return
