from numpy import absolute, asarray, full, linspace, minimum, nan
from statsmodels.sandbox.distributions.extras import ACSkewT_gen

from ._compute_context_indices import _compute_context_indices
from .check_nd_array_for_bad import check_nd_array_for_bad
from .fit_skew_t_pdf import fit_skew_t_pdf
from .make_coordinates_for_reflection import make_coordinates_for_reflection


def compute_context(
    _1d_array,
    n_data=None,
    location=None,
    scale=None,
    degree_of_freedom=None,
    shape=None,
    fit_initial_location=None,
    fit_initial_scale=None,
    n_grid=1e3,
    degree_of_freedom_for_tail_reduction=1e8,
    multiply_distance_from_reference_argmax=False,
    global_location=None,
    global_scale=None,
    global_degree_of_freedom=None,
    global_shape=None,
):

    is_bad = check_nd_array_for_bad(_1d_array, raise_for_bad=False)

    _1d_array_good = _1d_array[~is_bad]

    if any(
        parameter is None
        for parameter in (n_data, location, scale, degree_of_freedom, shape)
    ):

        n_data, location, scale, degree_of_freedom, shape = fit_skew_t_pdf(
            _1d_array_good,
            fit_initial_location=fit_initial_location,
            fit_initial_scale=fit_initial_scale,
        )

    grid = linspace(_1d_array_good.min(), _1d_array_good.max(), n_grid)

    skew_t_model = ACSkewT_gen()

    pdf = skew_t_model.pdf(grid, degree_of_freedom, shape, loc=location, scale=scale)

    shape_pdf_reference = minimum(
        pdf,
        skew_t_model.pdf(
            make_coordinates_for_reflection(grid, grid[pdf.argmax()]),
            degree_of_freedom_for_tail_reduction,
            shape,
            loc=location,
            scale=scale,
        ),
    )

    shape_context_indices = _compute_context_indices(
        grid, pdf, shape_pdf_reference, multiply_distance_from_reference_argmax
    )

    if any(
        parameter is None
        for parameter in (
            global_location,
            global_scale,
            global_degree_of_freedom,
            global_shape,
        )
    ):

        location_pdf_reference = None

        location_context_indices = None

        context_indices = shape_context_indices

    else:

        location_pdf_reference = minimum(
            pdf,
            skew_t_model.pdf(
                grid,
                global_degree_of_freedom,
                global_shape,
                loc=global_location,
                scale=global_scale,
            ),
        )

        location_context_indices = _compute_context_indices(
            grid, pdf, location_pdf_reference, multiply_distance_from_reference_argmax
        )

        context_indices = shape_context_indices + location_context_indices

    context_indices_like_array = full(_1d_array.size, nan)

    context_indices_like_array[~is_bad] = context_indices[
        [absolute(grid - value).argmin() for value in _1d_array_good]
    ]

    return {
        "fit": asarray((n_data, location, scale, degree_of_freedom, shape)),
        "grid": grid,
        "pdf": pdf,
        "shape_pdf_reference": shape_pdf_reference,
        "shape_context_indices": shape_context_indices,
        "location_pdf_reference": location_pdf_reference,
        "location_context_indices": location_context_indices,
        "context_indices": context_indices,
        "context_indices_like_array": context_indices_like_array,
    }
