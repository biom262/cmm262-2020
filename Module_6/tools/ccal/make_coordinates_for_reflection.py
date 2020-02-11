from .check_nd_array_for_bad import check_nd_array_for_bad


def make_coordinates_for_reflection(
    coordinates, reflection_coordinate, raise_for_bad=True
):

    check_nd_array_for_bad(coordinates, raise_for_bad=raise_for_bad)

    coordinates_for_reflection = coordinates.copy()

    for i, coordinate in enumerate(coordinates_for_reflection):

        if coordinate < reflection_coordinate:

            coordinates_for_reflection[i] += (reflection_coordinate - coordinate) * 2

        else:

            coordinates_for_reflection[i] -= (coordinate - reflection_coordinate) * 2

    return coordinates_for_reflection
