from numpy import full, nan
from pandas import DataFrame, Index

from ._cluster_clustering_x_element_and_compute_ccc import (
    _cluster_clustering_x_element_and_compute_ccc,
)
from .mf_by_multiplicative_update import mf_by_multiplicative_update
from .nmf_by_sklearn import nmf_by_sklearn
from .plot_heat_map import plot_heat_map


def mf_consensus_cluster(
    df,
    k,
    mf_function="nmf_by_sklearn",
    n_clustering=10,
    n_iteration=int(1e3),
    random_seed=20121020,
    linkage_method="ward",
    plot_w=True,
    plot_h=True,
    plot_df=True,
    directory_path=None,
):

    print("MFCC with K={} ...".format(k))

    clustering_x_w_element = full((n_clustering, df.shape[0]), nan)

    clustering_x_h_element = full((n_clustering, df.shape[1]), nan)

    n_per_print = max(1, n_clustering // 10)

    if mf_function == "mf_by_multiplicative_update":

        mf_function = mf_by_multiplicative_update

    elif mf_function == "nmf_by_sklearn":

        mf_function = nmf_by_sklearn

    for clustering in range(n_clustering):

        if clustering % n_per_print == 0:

            print("\t(K={}) {}/{} ...".format(k, clustering + 1, n_clustering))

        w, h, e = mf_function(
            df.values, k, n_iteration=n_iteration, random_seed=random_seed + clustering
        )

        if clustering == 0:

            w_0 = w

            h_0 = h

            e_0 = e

            factors = Index(("F{}".format(i) for i in range(k)), name="Factor")

            w_0 = DataFrame(w_0, index=df.index, columns=factors)

            h_0 = DataFrame(h_0, index=factors, columns=df.columns)

            if directory_path is not None:

                w_0.to_csv("{}/w.tsv".format(directory_path), sep="\t")

                h_0.to_csv("{}/h.tsv".format(directory_path), sep="\t")

            if plot_w:

                print("Plotting w ...")

                file_name = "w.html"

                if directory_path is None:

                    html_file_path = None

                else:

                    html_file_path = "{}/{}".format(directory_path, file_name)

                plot_heat_map(
                    w_0,
                    normalization_axis=1,
                    normalization_method="-0-",
                    cluster_axis=0,
                    title="MF K{} W".format(k),
                    xaxis_title=w_0.columns.name,
                    yaxis_title=w_0.index.name,
                    html_file_path=html_file_path,
                )

            if plot_h:

                print("Plotting h ...")

                file_name = "h.html"

                if directory_path is None:

                    html_file_path = None

                else:

                    html_file_path = "{}/{}".format(directory_path, file_name)

                plot_heat_map(
                    h_0,
                    normalization_axis=0,
                    normalization_method="-0-",
                    cluster_axis=1,
                    title="MF K{} H".format(k),
                    xaxis_title=h_0.columns.name,
                    yaxis_title=h_0.index.name,
                    html_file_path=html_file_path,
                )

        clustering_x_w_element[clustering, :] = w.argmax(axis=1)

        clustering_x_h_element[clustering, :] = h.argmax(axis=0)

    w_element_cluster, w_element_cluster__ccc = _cluster_clustering_x_element_and_compute_ccc(
        clustering_x_w_element, k, linkage_method
    )

    h_element_cluster, h_element_cluster__ccc = _cluster_clustering_x_element_and_compute_ccc(
        clustering_x_h_element, k, linkage_method
    )

    if plot_df:

        print("Plotting df ...")

        file_name = "cluster.html"

        if directory_path is None:

            html_file_path = None

        else:

            html_file_path = "{}/{}".format(directory_path, file_name)

        plot_heat_map(
            df,
            normalization_axis=0,
            normalization_method="-0-",
            row_annotation=w_element_cluster,
            column_annotation=h_element_cluster,
            title="MFCC K={} W H Element Cluster".format(k),
            xaxis_title=df.columns.name,
            yaxis_title=df.index.name,
            html_file_path=html_file_path,
        )

    return (
        w_0,
        h_0,
        e_0,
        w_element_cluster,
        w_element_cluster__ccc,
        h_element_cluster,
        h_element_cluster__ccc,
    )
