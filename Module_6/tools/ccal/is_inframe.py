def is_inframe(ref, alt):

    return not ((len(ref) - len(alt)) % 3)
