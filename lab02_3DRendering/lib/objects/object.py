from lib.screen import Screen
from numpy.typing import ArrayLike


class Object:

    def transform(self, matrix: ArrayLike) -> None:
        '''
        Applies transformation to all coordinates of object

        Keyword arguments:
        matrix -- transformation matrix
        '''
        pass

    def draw(self, screen: Screen) -> None:
        '''
        Draws object on canvas and zbuffer

        Keyword arguments:
        screen -- screen object
        '''
        pass
