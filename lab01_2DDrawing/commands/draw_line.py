import numpy as np


def reflect_vertically(arr: np.array) -> np.array:

    # initialize result
    reflected = np.zeros(arr.shape, dtype=arr.dtype)

    # get number of rows
    rows_n = arr.shape[0]

    # update array
    for i in range(arr.shape[0]):
        reflected[rows_n - i - 1] = arr[i]

    # return reflected array
    return reflected


def reflect_x_equals_y(arr: np.array) -> np.array:

    # initialize result
    reflected = np.zeros((arr.shape[1], arr.shape[0], arr.shape[2]),
                         dtype=arr.dtype)

    # update array
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            reflected[arr.shape[1] - j - 1, arr.shape[0] - i - 1] = arr[i, j]

    # return reflected array
    return reflected


def draw_line(image: np.array,
              pen_color: np.array,
              matrix: np.array,
              x0: int,
              y0: int,
              x1: int,
              y1: int) -> np.array:
    # get image parameters
    height, width, _ = image.shape

    # get pixel color
    color = (pen_color[0], pen_color[1], pen_color[2])

    # apply transformation
    start = matrix.dot(np.array([int(x0), int(y0), 1], dtype=matrix.dtype))
    end = matrix.dot(np.array([int(x1), int(y1), 1], dtype=matrix.dtype))

    # convert parameters to int
    x0 = round(start[0]/start[2])
    y0 = round(start[1]/start[2])
    x1 = round(end[0]/end[2])
    y1 = round(end[1]/end[2])

    # check image bounds
    assert x0 >= 0 and x0 < width and x1 >= 0 and x1 < width and \
           y0 >= 0 and y0 < height and y1 >= 0 and y1 < height

    # get coordinates deltas
    dx = x1 - x0
    dy = y1 - y0

    # slope bigger than 1: reflect over plane x = y
    reflected_x_equals_y = False
    if abs(dy) > abs(dx):

        # update new line parameters
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        dx = x1 - x0
        dy = y1 - y0
        height, width = width, height

        # reflect image
        image = reflect_x_equals_y(image)
        reflected_x_equals_y = True

    # going from right to left: reflect direction
    if dx < 0:

        # update new line parameters
        x0, x1 = x1, x0
        y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0

    # negative slope: reflect vertically
    reflected_vertically = False
    if dy < 0:

        # update new line parameters
        y0, y1 = height - 1 - y0, height - 1 - y1
        dy = y1 - y0

        # reflect image
        image = reflect_vertically(image)
        reflected_vertically = True

    # midpoint algorithm considering the simple case:
    #   * x1 > x0;
    #   * dy/dx between 0 and 1

    # decision variable
    D = dy + dy - dx
    for x_iter in range(x0, x1+1):
        # draws pixel
        # y0 is converted to image (row, col) coordinates
        image[height - 1 - y0, x_iter] = color
        # NE
        if (D > 0):
            y0 += 1
        # update decision variable
        delta = dy + dy if D <= 0 else dy + dy - dx - dx
        D += delta

    # vertically reflected image: reflect again to revert
    if reflected_vertically:
        image = reflect_vertically(image)

    # reflected image over plane x = y: reflect again to revert
    if reflected_x_equals_y:
        image = reflect_x_equals_y(image)

    # return image
    return image, matrix
