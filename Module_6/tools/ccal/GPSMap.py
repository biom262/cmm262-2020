from numpy import diag, full, issubdtype, linspace, mean, nan, number
from pandas import DataFrame, Series
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist, squareform

from ._anneal_node_and_element_positions import _anneal_node_and_element_positions
from ._check_node_x_element import _check_node_x_element
from ._check_w_or_h import _check_w_or_h
from ._make_element_x_dimension import _make_element_x_dimension
from ._make_grid_values_and_categorical_labels import (
    _make_grid_values_and_categorical_labels,
)
from ._plot_gps_map import _plot_gps_map
from .apply_function_on_2_2d_arrays_slices import apply_function_on_2_2d_arrays_slices
from .COLOR_CATEGORICAL import COLOR_CATEGORICAL
from .compute_information_distance import compute_information_distance
from .mds import mds
from .normalize_nd_array import normalize_nd_array
from .plot_heat_map import plot_heat_map
from .train_and_classify import train_and_classify

element_marker_size = 16

grid_label_opacity_without_annotation = 0.64

grid_label_opacity_with_annotation = grid_label_opacity_without_annotation * 0.64


class GPSMap:
    def __init__(
        self,
        w=None,
        h=None,
        function_to_blend_node_node_distance=mean,
        node_x_dimension=None,
        mds_random_seed=20121020,
        w_n_pull=None,
        w_pull_power=None,
        h_n_pull=None,
        h_pull_power=None,
        plot=True,
    ):

        self.w = None

        self.h = None

        self.nodes = None

        self.node_name = None

        self.w_elements = None

        self.w_element_name = None

        self.w_distance__node_x_node = None

        self.h_elements = None

        self.h_element_name = None

        self.h_distance__node_x_node = None

        self.distance__node_x_node = None

        self.node_x_dimension = node_x_dimension

        self.triangulation = None

        self.w_n_pull = w_n_pull

        self.w_pull_power = w_pull_power

        self.w_element_x_dimension = None

        self.h_n_pull = h_n_pull

        self.h_pull_power = h_pull_power

        self.h_element_x_dimension = None

        self.n_grid = None

        self.mask_grid = None

        self.w_element_labels = None

        self.w_labels = None

        self.w_bandwidth_factor = None

        self.w_grid_values = None

        self.w_grid_labels = None

        self.w_label_colors = None

        self.h_element_labels = None

        self.h_labels = None

        self.h_bandwidth_factor = None

        self.h_grid_values = None

        self.h_grid_labels = None

        self.h_label_colors = None

        self.w_distance__element_x_element = None

        self.w_distance__node_x_element = None

        self.h_distance__element_x_element = None

        self.h_distance__node_x_element = None

        if w is not None:

            _check_node_x_element(w)

        if h is not None:

            _check_node_x_element(h)

        if w is not None and h is not None:

            if (w.index == h.index).all() and w.index.name == h.index.name:

                self.nodes = w.index.tolist()

                self.node_name = w.index.name

            else:

                raise ValueError("w and h indices mismatch.")

        elif w is not None:

            self.nodes = w.index.tolist()

        elif h is not None:

            self.nodes = h.index.tolist()

        if w is not None:

            self.w = w.values

            self.w_elements = w.columns.tolist()

            self.w_element_name = w.columns.name

            if plot:

                plot_heat_map(
                    DataFrame(self.w, index=self.nodes, columns=self.w_elements),
                    normalization_axis=0,
                    normalization_method="-0-",
                    cluster_axis=1,
                    title="W",
                    xaxis_title=self.w_element_name,
                    yaxis_title=self.node_name,
                )

            self.w_distance__node_x_node = squareform(
                pdist(self.w, metric=compute_information_distance)
            )

            if plot:

                plot_heat_map(
                    DataFrame(
                        self.w_distance__node_x_node,
                        index=self.nodes,
                        columns=self.nodes,
                    ),
                    cluster_axis="01",
                    title="{0}-{0} Distance in W".format(self.node_name),
                    xaxis_title=self.node_name,
                    yaxis_title=self.node_name,
                )

        if h is not None:

            self.h = h.values

            self.h_elements = h.columns.tolist()

            self.h_element_name = h.columns.name

            if plot:

                plot_heat_map(
                    DataFrame(self.h, index=self.nodes, columns=self.h_elements),
                    normalization_axis=0,
                    normalization_method="-0-",
                    cluster_axis=1,
                    title="H",
                    xaxis_title=self.h_element_name,
                    yaxis_title=self.node_name,
                )

            self.h_distance__node_x_node = squareform(
                pdist(self.h, metric=compute_information_distance)
            )

            if plot:

                plot_heat_map(
                    DataFrame(
                        self.h_distance__node_x_node,
                        index=self.nodes,
                        columns=self.nodes,
                    ),
                    cluster_axis="01",
                    title="{0}-{0} Distance in H".format(self.node_name),
                    xaxis_title=self.node_name,
                    yaxis_title=self.node_name,
                )

        if w is not None and h is not None:

            self.distance__node_x_node = full((len(self.nodes),) * 2, nan)

            for i in range(len(self.nodes)):

                for j in range(len(self.nodes)):

                    self.distance__node_x_node[
                        i, j
                    ] = function_to_blend_node_node_distance(
                        (
                            self.w_distance__node_x_node[i, j],
                            self.h_distance__node_x_node[i, j],
                        )
                    )

            if plot:

                plot_heat_map(
                    DataFrame(
                        self.distance__node_x_node, index=self.nodes, columns=self.nodes
                    ),
                    cluster_axis="01",
                    title="{0}-{0} Distance in W and H".format(self.node_name),
                    xaxis_title=self.node_name,
                    yaxis_title=self.node_name,
                )

        elif w is not None:

            self.distance__node_x_node = self.w_distance__node_x_node

        elif h is not None:

            self.distance__node_x_node = self.h_distance__node_x_node

        if self.node_x_dimension is None:

            self.node_x_dimension = normalize_nd_array(
                mds(
                    2,
                    distance__point_x_point=self.distance__node_x_node,
                    random_seed=mds_random_seed,
                ),
                0,
                "0-1",
            )

        self.triangulation = Delaunay(self.node_x_dimension)

        if w is not None:

            self.w_element_x_dimension = _make_element_x_dimension(
                self.w, self.node_x_dimension, self.w_n_pull, self.w_pull_power
            )

        if h is not None:

            self.h_element_x_dimension = _make_element_x_dimension(
                self.h, self.node_x_dimension, self.h_n_pull, self.h_pull_power
            )

    def set_element_labels(
        self,
        w_or_h,
        element_labels,
        n_grid=128,
        bandwidth_factor=1,
        label_colors=None,
        plot=True,
    ):

        _check_w_or_h(w_or_h)

        if not issubdtype(element_labels, number):

            raise ValueError("element_labels should be only number.")

        if (element_labels.value_counts() < 3).any():

            raise ValueError("A label should not have less than 3 elements.")

        if w_or_h == "w":

            element_x_dimension = self.w_element_x_dimension

        elif w_or_h == "h":

            element_x_dimension = self.h_element_x_dimension

        self.n_grid = n_grid

        self.mask_grid = full((n_grid,) * 2, nan)

        x_grid_for_j = linspace(0, 1, self.n_grid)

        y_grid_for_i = linspace(1, 0, self.n_grid)

        for i in range(n_grid):

            for j in range(n_grid):

                self.mask_grid[i, j] = (
                    self.triangulation.find_simplex((x_grid_for_j[j], y_grid_for_i[i]))
                    == -1
                )

        labels = sorted(element_labels.unique())

        grid_values, grid_labels = _make_grid_values_and_categorical_labels(
            element_x_dimension,
            element_labels,
            self.n_grid,
            bandwidth_factor,
            self.mask_grid,
        )

        if label_colors is None:

            label_colors = COLOR_CATEGORICAL[: element_labels.unique().size]

        if w_or_h == "w":

            self.w_element_labels = element_labels

            self.w_labels = labels

            self.w_bandwidth_factor = bandwidth_factor

            self.w_grid_values = grid_values

            self.w_grid_labels = grid_labels

            self.w_label_colors = label_colors

        elif w_or_h == "h":

            self.h_element_labels = element_labels

            self.h_labels = labels

            self.h_bandwidth_factor = bandwidth_factor

            self.h_grid_values = grid_values

            self.h_grid_labels = grid_labels

            self.h_label_colors = label_colors

        if plot:

            if w_or_h == "w":

                z = DataFrame(self.w, index=self.nodes, columns=self.w_elements)

                column_annotation = self.w_element_labels

                element_name = self.w_element_name

            elif w_or_h == "h":

                z = DataFrame(self.h, index=self.nodes, columns=self.h_elements)

                column_annotation = self.h_element_labels

                element_name = self.h_element_name

            plot_heat_map(
                z,
                normalization_axis=0,
                normalization_method="-0-",
                column_annotation=column_annotation,
                column_annotation_colors=label_colors,
                title=w_or_h.title(),
                xaxis_title=element_name,
                yaxis_title=self.node_name,
            )

    def plot_gps_map(
        self,
        w_or_h,
        grid_label_opacity=None,
        annotation_x_element=None,
        annotation_types=None,
        annotation_std_maxs=None,
        annotation_ranges=None,
        annotation_colorscale=None,
        elements_to_be_emphasized=None,
        element_marker_size=element_marker_size,
        layout_size=880,
        title=None,
        html_file_path=None,
        plotly_html_file_path=None,
    ):

        _check_w_or_h(w_or_h)

        if w_or_h == "w":

            elements = self.w_elements

            element_name = self.w_element_name

            element_x_dimension = self.w_element_x_dimension

            element_labels = self.w_element_labels

            grid_values = self.w_grid_values

            grid_labels = self.w_grid_labels

            label_colors = self.w_label_colors

        elif w_or_h == "h":

            elements = self.h_elements

            element_name = self.h_element_name

            element_x_dimension = self.h_element_x_dimension

            element_labels = self.h_element_labels

            grid_values = self.h_grid_values

            grid_labels = self.h_grid_labels

            label_colors = self.h_label_colors

        if annotation_x_element is None:

            if grid_label_opacity is None:

                grid_label_opacity = grid_label_opacity_without_annotation

        else:

            annotation_x_element = annotation_x_element.reindex(columns=elements)

            if grid_label_opacity is None:

                grid_label_opacity = grid_label_opacity_with_annotation

        if title is None:

            title = w_or_h.title()

        _plot_gps_map(
            self.nodes,
            self.node_name,
            self.node_x_dimension,
            elements,
            element_name,
            element_x_dimension,
            element_marker_size,
            element_labels,
            grid_values,
            grid_labels,
            label_colors,
            grid_label_opacity,
            annotation_x_element,
            annotation_types,
            annotation_std_maxs,
            annotation_ranges,
            annotation_colorscale,
            layout_size,
            title,
            html_file_path,
            plotly_html_file_path,
        )

    def predict(
        self,
        w_or_h,
        w_or_h_df,
        support_vector_parameter_c=1e3,
        n_pull=None,
        pull_power=None,
        grid_label_opacity=None,
        annotation_x_element=None,
        annotation_types=None,
        annotation_std_maxs=None,
        annotation_ranges=None,
        annotation_colorscale=None,
        element_marker_size=element_marker_size,
        layout_size=880,
        title=None,
        html_file_path=None,
        plotly_html_file_path=None,
    ):

        _check_w_or_h(w_or_h)

        predicting_elements = w_or_h_df.columns

        if w_or_h == "w":

            node_x_element = self.w

            element_name = self.w_element_name

            if n_pull is None:

                n_pull = self.w_n_pull

            if pull_power is None:

                pull_power = self.w_pull_power

            element_labels = self.w_element_labels

            grid_values = self.w_grid_values

            grid_labels = self.w_grid_labels

            label_colors = self.w_label_colors

        elif w_or_h == "h":

            node_x_element = self.h

            element_name = self.h_element_name

            if n_pull is None:

                n_pull = self.h_n_pull

            if pull_power is None:

                pull_power = self.h_pull_power

            element_labels = self.h_element_labels

            grid_values = self.h_grid_values

            grid_labels = self.h_grid_labels

            label_colors = self.h_label_colors

        predicting_element_x_dimension = _make_element_x_dimension(
            w_or_h_df.values, self.node_x_dimension, n_pull, pull_power
        )

        if element_labels is not None:

            predicted_element_labels = Series(
                train_and_classify(
                    node_x_element.T,
                    element_labels,
                    w_or_h_df.T,
                    c=support_vector_parameter_c,
                    tol=1e-8,
                ),
                name="Predicted {} Element Label".format(element_name),
                index=predicting_elements,
            )

        else:

            predicted_element_labels = None

        if annotation_x_element is None:

            if grid_label_opacity is None:

                grid_label_opacity = grid_label_opacity_without_annotation

        else:

            annotation_x_element = annotation_x_element.reindex(
                columns=predicting_elements
            )

            if grid_label_opacity is None:

                grid_label_opacity = grid_label_opacity_with_annotation

        if title is None:

            title = "{} (predicted)".format(w_or_h.title())

        _plot_gps_map(
            self.nodes,
            self.node_name,
            self.node_x_dimension,
            predicting_elements,
            element_name,
            predicting_element_x_dimension,
            element_marker_size,
            predicted_element_labels,
            grid_values,
            grid_labels,
            label_colors,
            grid_label_opacity,
            annotation_x_element,
            annotation_types,
            annotation_std_maxs,
            annotation_ranges,
            annotation_colorscale,
            layout_size,
            title,
            html_file_path,
            plotly_html_file_path,
        )

        return predicted_element_labels

    def anneal_node_and_element_positions(
        self,
        w_or_h,
        node_node_score_weight=0,
        element_element_score_weight=0.5,
        node_element_score_weight=0.5,
        n_fraction_node_to_move=1,
        n_fraction_element_to_move=1,
        random_seed=20121020,
        n_iteration=int(1e3),
        initial_temperature=1e-4,
        scale=1e-3,
        triangulate=True,
        print_acceptance=True,
    ):

        _check_w_or_h(w_or_h)

        if w_or_h == "w":

            if self.w_distance__element_x_element is None:

                self.w_distance__element_x_element = squareform(
                    pdist(self.w.T, metric=compute_information_distance)
                )

            distance__element_x_element = self.w_distance__element_x_element

            if self.w_distance__node_x_element is None:

                distance__w_ielement_x_node = apply_function_on_2_2d_arrays_slices(
                    self.w,
                    diag((1,) * len(self.nodes)),
                    compute_information_distance,
                    0,
                )

                distance__node_x_w_ielement = apply_function_on_2_2d_arrays_slices(
                    self.w,
                    diag((1,) * len(self.w_elements)),
                    compute_information_distance,
                    1,
                )

                self.w_distance__node_x_element = (
                    distance__w_ielement_x_node.T + distance__node_x_w_ielement
                ) / 2

            distance__node_x_element = self.w_distance__node_x_element

            element_x_dimension = self.w_element_x_dimension

        elif w_or_h == "h":

            if self.h_distance__element_x_element is None:

                self.h_distance__element_x_element = squareform(
                    pdist(self.h.T, metric=compute_information_distance)
                )

            distance__element_x_element = self.h_distance__element_x_element

            if self.h_distance__node_x_element is None:

                distance__h_ielement_x_node = apply_function_on_2_2d_arrays_slices(
                    self.h,
                    diag((1,) * len(self.nodes)),
                    compute_information_distance,
                    0,
                )

                distance__node_x_h_ielement = apply_function_on_2_2d_arrays_slices(
                    self.h,
                    diag((1,) * len(self.h_elements)),
                    compute_information_distance,
                    1,
                )

                self.h_distance__node_x_element = (
                    distance__h_ielement_x_node.T + distance__node_x_h_ielement
                ) / 2

            distance__node_x_element = self.h_distance__node_x_element

            element_x_dimension = self.h_element_x_dimension

        node_x_dimension, element_x_dimension = _anneal_node_and_element_positions(
            self.distance__node_x_node,
            distance__element_x_element,
            distance__node_x_element,
            self.node_x_dimension,
            element_x_dimension,
            node_node_score_weight,
            element_element_score_weight,
            node_element_score_weight,
            n_fraction_node_to_move,
            n_fraction_element_to_move,
            random_seed,
            n_iteration,
            initial_temperature,
            scale,
            triangulate,
            print_acceptance,
        )

        self.node_x_dimension = normalize_nd_array(node_x_dimension, 0, "0-1")

        if w_or_h == "w":

            self.w_element_x_dimension = element_x_dimension

            element_labels = self.w_element_labels

            bandwidth_factor = self.w_bandwidth_factor

        elif w_or_h == "h":

            self.h_element_x_dimension = element_x_dimension

            element_labels = self.h_element_labels

            bandwidth_factor = self.h_bandwidth_factor

        self.set_element_labels(
            w_or_h,
            element_labels,
            n_grid=self.n_grid,
            bandwidth_factor=bandwidth_factor,
            plot=False,
        )
