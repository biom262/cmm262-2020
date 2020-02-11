def str_is_version(str_):

    return (
        "." in str_
        and len(str_.split(sep=".")) == 3
        and all(i.isnumeric() for i in str_.split(sep="."))
    )
