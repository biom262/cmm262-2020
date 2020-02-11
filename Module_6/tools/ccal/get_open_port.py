from socket import AF_INET, SOCK_STREAM, socket


def get_open_port():

    with socket(AF_INET, SOCK_STREAM) as socket_:

        socket_.bind(("", 0))

        return socket_.getsockname()[1]
