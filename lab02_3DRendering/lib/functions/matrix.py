import numpy as np


def set_matrix(image: np.array,
               pen_color: np.array,
               matrix: np.array,
               *args: list) -> (np.array, np.array):
    '''
    Sets new matrix based on args input

    Keyword arguments:
    image -- numpy matrix object to paint on
    pen_color -- rgb color vector to paint with
    matrix -- old linear transformation
    *args -- 9 floats of the matrix in the format [a, b, c, d, e, f, g, h, i]
    for the new matrix:
        a b c
        d e f
        g h i
    '''

    # convert parameters to float
    args = list(map(float, args))

    # not enough args: fail
    assert len(args) == 9

    # return image
    return image, np.array([args[0:3], args[3:6], args[6:9]])


def multiply_matrix(image: np.array,
                    pen_color: np.array,
                    matrix: np.array,
                    *args: list) -> (np.array, np.array):
    '''
    Multiplies old matrix A with new matrix B in the order A x B

    Keyword arguments:
    image -- numpy matrix object to paint on
    pen_color -- rgb color vector to paint with
    matrix -- old linear transformation
    *args -- 9 floats of the matrix in the format [a, b, c, d, e, f, g, h, i]
    for the matrix to multiply with:
        a b c
        d e f
        g h i
    '''

    # convert parameters to float
    args = list(map(float, args))

    # not enough args: fail
    assert len(args) == 9

    # return image
    return image, matrix.dot(np.array([args[0:3], args[3:6], args[6:9]]))
