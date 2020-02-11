from scipy.spatial import Delaunay


def _get_triangulation_edges(point_x_dimension):

    edge_xs = []

    edge_ys = []

    triangulation = Delaunay(point_x_dimension)

    for (point_0_index, point_1_index, point_2_index) in triangulation.simplices:

        point_0 = triangulation.points[point_0_index]

        point_1 = triangulation.points[point_1_index]

        point_2 = triangulation.points[point_2_index]

        edge_xs.append(point_0[0])

        edge_xs.append(point_1[0])

        edge_xs.append(point_2[0])

        edge_xs.append(None)

        edge_ys.append(point_0[1])

        edge_ys.append(point_1[1])

        edge_ys.append(point_2[1])

        edge_ys.append(None)

    for (point_0_index, point_1_index) in triangulation.convex_hull:

        point_0 = triangulation.points[point_0_index]

        point_1 = triangulation.points[point_1_index]

        edge_xs.append(point_0[0])

        edge_xs.append(point_1[0])

        edge_xs.append(None)

        edge_ys.append(point_0[1])

        edge_ys.append(point_1[1])

        edge_ys.append(None)

    return edge_xs, edge_ys
