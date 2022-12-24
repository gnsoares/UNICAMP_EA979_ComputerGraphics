import numpy as np

from numpy.typing import ArrayLike
from numpy.typing import DTypeLike


# canvas constants
CHANNELS_N = 3
IMAGE_DTYPE = np.uint8
BACKGROUND = np.full(CHANNELS_N, fill_value=255, dtype=IMAGE_DTYPE)
PEN = np.full(CHANNELS_N, fill_value=0, dtype=IMAGE_DTYPE)

# z-buffer constants
ZBUFFER_DTYPE = np.float64
ZBUFFER_BACKGROUND = -np.inf


class Screen:

    def __init__(self,
                 width: int,
                 height: int,
                 channels: int = CHANNELS_N,
                 background: ArrayLike = BACKGROUND,
                 pen: ArrayLike = PEN,
                 dtype: DTypeLike = IMAGE_DTYPE):
        '''
        Screen object

        Keyword arguments:
        width -- screen width in pixels
        height -- screen height in pixels
        channels -- number of image channels
        background -- image background color (dimension must match channels)
        pen -- pen color (dimension must match channels)
        dtype -- image numpy array dtype
        '''
        self.pen = pen
        self.canvas = np.full(
            (height, width, channels),
            fill_value=background,
            dtype=dtype
        )
        self.zbuffer = np.full(
            (height, width),
            fill_value=ZBUFFER_BACKGROUND,
            dtype=ZBUFFER_DTYPE
        )
        self.viewport = np.identity(4, dtype=np.float32)

    def replace_viewport(self, matrix: ArrayLike):
        '''
        Replace viewport matrix

        Keyword arguments:
        matrix -- matrix to replace
        '''
        self.viewport = matrix

    def reset(self, color: ArrayLike):
        '''
        Sets canvas as plain background color

        Keyword arguments:
        color -- rgb color
        '''
        self.canvas = np.full(
            self.canvas.shape,
            fill_value=color,
            dtype=self.canvas.dtype
        )

    def set_pen_color(self, color: ArrayLike):
        '''
        Sets current pen color

        Keyword arguments:
        color -- rgb color
        '''
        self.pen = color
