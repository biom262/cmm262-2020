from numpy import absolute, concatenate, cumsum, inf

from .compute_kullback_leibler_divergence import compute_kullback_leibler_divergence


def _compute_context_indices(
    grid, pdf, pdf_reference, multiply_distance_from_reference_argmax
):

    center = pdf_reference.argmax()

    left_kl = compute_kullback_leibler_divergence(pdf[:center], pdf_reference[:center])

    right_kl = compute_kullback_leibler_divergence(pdf[center:], pdf_reference[center:])

    left_kl[left_kl == inf] = 0

    right_kl[right_kl == inf] = 0

    left_context_indices = -cumsum((left_kl / left_kl.sum())[::-1])[::-1]

    right_context_indices = cumsum(right_kl / right_kl.sum())

    left_context_indices *= left_kl.sum() / left_kl.size

    right_context_indices *= right_kl.sum() / right_kl.size

    context_indices = concatenate((left_context_indices, right_context_indices))

    if multiply_distance_from_reference_argmax:

        context_indices *= absolute(grid - grid[center])

    return context_indices
