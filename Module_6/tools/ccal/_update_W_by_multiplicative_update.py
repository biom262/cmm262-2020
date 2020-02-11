def _update_W_by_multiplicative_update(V, W, H):

    return W * (V @ H.T) / (W @ H @ H.T)
