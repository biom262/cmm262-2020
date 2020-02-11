from datetime import datetime


def get_now(only_time=False):

    if only_time:

        formatter = "%H:%M:%S"

    else:

        formatter = "%Y-%m-%d %H:%M:%S"

    return datetime.now().strftime(formatter)
