import numpy as np

from commands.polyline import polyline


def polygon(image: np.array,
            pen_color: np.array,
            matrix: np.array,
            n: str,
            *args: list) -> (np.array, np.array):
    '''
    Draw a sequence of lines starting from where the last one ended and
    finishing at the start

    Keyword arguments:
    image -- numpy matrix object to paint on
    pen_color -- rgb color vector to paint with
    matrix -- linear transformation to apply
    n -- number of arguments
    *args -- pairs (x, y) representing points
    '''
    return polyline(image,
                    pen_color,
                    matrix,
                    int(n) + 1,
                    *args,
                    args[0],
                    args[1])
