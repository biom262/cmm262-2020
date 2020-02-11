def log_and_return_response(response, logger=None):

    str_ = response.get_data().decode().strip()

    if logger is None:

        print(str_)

    else:

        logger.debug(str_)

    return response
