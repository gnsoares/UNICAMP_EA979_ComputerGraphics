import numpy as np


def change_color(image: np.array,
                 pen_color: np.array,
                 matrix: np.array,
                 r: str,
                 g: str,
                 b: str) -> np.array:
    '''
    Changes pen color

    Keyword arguments:
    image -- numpy matrix object to paint on
    pen_color -- rgb color vector to paint with
    matrix -- linear transformation (not used, present just to follow parrern)
    r -- red value
    g -- green value
    b -- blue value
    '''

    # change pen red, green and blue parameters
    pen_color[0] = int(r)
    pen_color[1] = int(g)
    pen_color[2] = int(b)

    # return image
    return image, matrix
