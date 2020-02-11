from sklearn.decomposition import NMF


def nmf_by_sklearn(
    V, k, solver="cd", tol=1e-8, n_iteration=int(1e3), random_seed=20121020
):

    model = NMF(
        n_components=k,
        solver=solver,
        tol=tol,
        max_iter=n_iteration,
        random_state=random_seed,
    )

    W = model.fit_transform(V)

    H = model.components_

    R_norm = model.reconstruction_err_

    return W, H, R_norm
