import numpy as np


def paint_screen(image: np.array,
                 pen_color: np.array,
                 matrix: np.array,
                 r: str,
                 g: str,
                 b: str) -> np.array:
    '''
    Paint entire screen with color

    Keyword arguments:
    image -- numpy matrix object to paint on
    pen_color -- rgb color vector to paint with
    matrix -- linear transformation (not used, present just to follow parrern)
    r -- red value
    g -- green value
    b -- blue value
    '''
    # get new image color
    color = np.array([int(r), int(g), int(b)])

    # return image
    return np.full(image.shape, fill_value=color, dtype=np.uint8), matrix
