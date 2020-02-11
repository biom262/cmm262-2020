from scipy.cluster.hierarchy import cophenet, fcluster, linkage
from scipy.spatial.distance import squareform

from ._get_coclustering_portion import _get_coclustering_portion


def _cluster_clustering_x_element_and_compute_ccc(
    clustering_x_element, k, linkage_method
):

    clustering_distance = squareform(
        1 - _get_coclustering_portion(clustering_x_element)
    )

    clustering_distance_linkage = linkage(clustering_distance, method=linkage_method)

    return (
        fcluster(clustering_distance_linkage, k, criterion="maxclust") - 1,
        cophenet(clustering_distance_linkage, clustering_distance)[0],
    )
