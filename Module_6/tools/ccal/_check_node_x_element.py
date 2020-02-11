from numpy import issubdtype, number
from pandas import DataFrame

from .check_nd_array_for_bad import check_nd_array_for_bad


def _check_node_x_element(node_x_element):

    if not isinstance(node_x_element, DataFrame):

        raise ValueError("node_x_element should be a DataFrame.")

    if node_x_element.index.has_duplicates:

        raise ValueError("node_x_element should not have duplicated node.")

    if node_x_element.columns.has_duplicates:

        raise ValueError("node_x_element should not have duplicated element.")

    if not all(
        issubdtype(series, number) for node, series in node_x_element.iterrows()
    ):

        raise ValueError("node_x_element should be only number.")

    check_nd_array_for_bad(node_x_element.values)
