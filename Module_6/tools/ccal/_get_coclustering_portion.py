from numpy import zeros


def _get_coclustering_portion(clustering_x_element):

    n_coclustering__element_x_element = zeros((clustering_x_element.shape[1],) * 2)

    for clustering in range(clustering_x_element.shape[0]):

        for element_0 in range(clustering_x_element.shape[1]):

            for element_1 in range(element_0, clustering_x_element.shape[1]):

                if element_0 == element_1:

                    n_coclustering__element_x_element[element_0, element_1] += 1

                elif (
                    clustering_x_element[clustering, element_0]
                    == clustering_x_element[clustering, element_1]
                ):

                    n_coclustering__element_x_element[element_0, element_1] += 1

                    n_coclustering__element_x_element[element_1, element_0] += 1

    return n_coclustering__element_x_element / clustering_x_element.shape[0]
