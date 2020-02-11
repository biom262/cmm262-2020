from numpy import sign, sqrt


def rescale_x_y_coordiantes_in_polar_coordiante(x, y, radius_rescaling_factor):

    x_sign = sign(x)

    y_sign = sign(y)

    x_y_ratio = x / y

    radius = sqrt(x ** 2 + y ** 2)

    x = (x_y_ratio * radius / radius_rescaling_factor) / sqrt(x_y_ratio ** 2 + 1)

    y = x / x_y_ratio

    if sign(x) != x_sign:

        x *= -1

    if sign(y) != y_sign:

        y *= -1

    return x, y
