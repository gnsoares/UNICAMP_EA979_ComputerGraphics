import numpy as np

from numpy.typing import ArrayLike
from queue import LifoQueue


class Tranformation:

    def __init__(self):
        '''
        Tranformation object
        '''
        self.current = np.identity(4, dtype=np.float32)
        self.stack = LifoQueue()

    def replace_current(self, matrix: ArrayLike) -> None:
        '''
        Replace current transformation matrix

        Keyword arguments:
        matrix -- matrix to replace current
        '''
        self.current = matrix

    def pop_transformation(self) -> None:
        '''
        Takes the transformation matrix on the the matrix transformation pile
        '''
        self.current = self.stack.get()

    def push_transformation(self) -> None:
        '''
        Adds a transformation matrix on the top of the matrix transformation pile
        '''
        self.stack.put(self.current)