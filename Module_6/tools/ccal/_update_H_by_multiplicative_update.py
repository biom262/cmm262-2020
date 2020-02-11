def _update_H_by_multiplicative_update(V, W, H):

    return H * (W.T @ V) / (W.T @ W @ H)
