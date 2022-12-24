import numpy as np

from commands.draw_line import draw_line


def polyline(image: np.array,
             pen_color: np.array,
             matrix: np.array,
             n: str,
             *args: list) -> (np.array, np.array):
    '''
    Draw a sequence of lines starting from where the last one ended

    Keyword arguments:
    image -- numpy matrix object to paint on
    pen_color -- rgb color vector to paint with
    matrix -- linear transformation to apply
    n -- number of arguments
    *args -- pairs (x, y) representing points
    '''

    # convert parameters to int
    n = int(n)
    args = list(map(int, args))

    # not enough args: fail
    assert len(args) == 2 * n

    # group desired points
    points = [(args[i], args[i + 1]) for i in range(0, len(args), 2)]

    # draw polyline
    current_point = points[0]
    for point in points[1:]:
        image, matrix = draw_line(image,
                                  pen_color,
                                  matrix,
                                  *current_point,
                                  *point)
        current_point = point

    # return image
    return image, matrix
