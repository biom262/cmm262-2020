def _check_w_or_h(w_or_h):

    if w_or_h not in ("w", "h"):
        raise ValueError("w_or_h should be either w or h.")
