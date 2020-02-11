from numpy import absolute, linspace, log2, sort

from .plot_and_save import plot_and_save
from .plot_points import plot_points


def plot_bayesian_nomogram(
    target,
    target_hit,
    target_miss,
    grid_size,
    conditional_probabilities,
    names,
    html_file_path=None,
    plotly_html_file_path=None,
):

    target_hit_probability = (target == target_hit).sum() / target.size

    target_miss_probability = (target == target_miss).sum() / target.size

    target_grid = linspace(target.min(), target.max(), grid_size)

    target_grid_hit_index = absolute(target_grid - target_hit).argmin()

    target_grid_miss_index = absolute(target_grid - target_miss).argmin()

    target = sort(target)[:: target.size // grid_size]

    grid_shape = (grid_size, grid_size)

    for conditional_probability in conditional_probabilities:

        if conditional_probability.shape != grid_shape:

            raise ValueError(
                "conditional_probability shape should be {}.".format(grid_shape)
            )

    layout = dict(
        width=960,
        height=80 * max(8, len(conditional_probabilities)),
        title="Bayesian Nomogram",
        yaxis=dict(
            zeroline=False, ticks="", showticklabels=False, title="Evidence", dtick=1
        ),
        xaxis=dict(title="Log Odds Ratio"),
        hovermode="closest",
    )

    data = []

    for i, (conditional_probability, name) in enumerate(
        zip(conditional_probabilities, names)
    ):

        target_hit_conditional_probability = conditional_probability[
            :, target_grid_hit_index
        ]

        target_miss_conditional_probability = conditional_probability[
            :, target_grid_miss_index
        ]

        log_odds_ratios = log2(
            (target_hit_conditional_probability / target_miss_conditional_probability)
            / (target_hit_probability / target_miss_probability)
        )

        plot_points(
            (tuple(range(grid_size)),) * 4,
            (
                target,
                target_hit_conditional_probability,
                target_miss_conditional_probability,
                log_odds_ratios,
            ),
            names=(
                name,
                "P(hit | {})".format(name),
                "P(miss | {})".format(name),
                "Log Odds Ratio",
            ),
            title=name,
            legend_orientation="h",
        )

        x = (log_odds_ratios.min(), log_odds_ratios.max())

        y = (i,) * 2

        data.append(dict(type="scatter", legendgroup=name, name=name, x=x, y=y))

    plot_and_save(dict(layout=layout, data=data), html_file_path, plotly_html_file_path)
