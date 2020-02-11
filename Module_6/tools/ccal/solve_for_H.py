from pandas import DataFrame

from .solve_ax_equal_b import solve_ax_equal_b


def solve_for_H(V, W, method="nnls"):

    print(
        "Solve for H in V{} = W{} * H{}.".format(
            V.shape, W.shape, (W.shape[1], V.shape[1])
        )
    )

    return DataFrame(
        solve_ax_equal_b(W.values, V.values, method=method),
        index=W.columns,
        columns=V.columns,
    )
